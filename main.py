from datetime import datetime, timedelta, timezone
import os
import pickle
from random import choice
import re
from re import Match
from time import sleep

import pytz
import requests
from rss_parser import RSSParser

from bookrss_schema import BookRSS
from simple_book import SimpleBook
from slack_bot import Message
from config import *


def read_user_ids() -> list[str]:
    ids: list[str] = []

    id_pattern = r"(?<=https://www.goodreads.com/user/show/)(\d+)"

    with open(user_links_name, "r") as user_links_file:
        for line in user_links_file.readlines():
            res: Match[str] | None = re.search(id_pattern, line)
            if res is not None:
                ids.append(res.group())

    return ids


def generate_user_link(id: str) -> str:
    return goodreads_rss_template % id


def load_goodreads_rss(url: str) -> requests.Response:
    resp: requests.Response = requests.get(url, headers=headers)
    return resp


def load_cachable_goodreads_rss(url: str, use_cache: bool) -> requests.Response:
    resp: requests.Response
    if use_cache:
        with open(cache_file, "rb") as cache:
            resp = pickle.load(cache)
    else:
        for link in user_links:
            resp = load_goodreads_rss(link)
            with open(cache_file, "wb") as cache:
                pickle.dump(resp, cache)
    return resp


def convert_rss_to_books(rss_text: str) -> set[SimpleBook]:
    books: set[SimpleBook] = set()
    rss = RSSParser.parse(rss_text, schema=BookRSS)
    for item in rss.channel.items:
        # print(f"Read at {item.user_read_at} {item.title.content}[{item.book_id}] written by {item.author_name.content}")
        read_date: datetime | None = as_date(item.user_read_at.content) if item.user_read_at else None
        books.add(SimpleBook(item.title.content, item.book_id.content, read_date))
    return books


def generate_user_file_name(user_id: str) -> str:
    return os.path.join(data_dir_name, user_id)


def load_user_history(user_id: str) -> set[SimpleBook]:
    user_file_name = generate_user_file_name(user_id)
    # If a user history has not been created, return an empty set
    if not os.path.exists(user_file_name):
        return set()

    with open(user_file_name, "rb") as user_file:
        return pickle.load(user_file)


def save_user_history(user_id: str, history: set[SimpleBook]) -> None:
    user_file_name = generate_user_file_name(user_id)
    with open(user_file_name, "wb") as user_file:
        pickle.dump(history, user_file)


def as_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")


def get_time_delta(date: datetime | None) -> timedelta:
    if date is None:
        return timedelta()
    return datetime.now(pytz.timezone("America/Chicago")) - date


if not os.path.exists(data_dir_name):
    os.mkdir(data_dir_name)

if not os.path.isdir(data_dir_name):
    raise Exception(f"Cannot create directory '{data_dir_name}'. Might already be a file. Please delete it or change data_dir_name")

user_ids = read_user_ids()
for id in user_ids:
    sleep(10)
    link = generate_user_link(id)
    print(f"Running for {id=} @ {link=}")

    user_history: set[SimpleBook] = load_user_history(id)

    resp: requests.Response = load_goodreads_rss(link)
    books: set[SimpleBook] = convert_rss_to_books(resp.text)

    print("\n".join(map(lambda x: str(x), list(books))))

    new_books: list[SimpleBook] = list(books - user_history)

    recent_new_books: list[SimpleBook] = list(filter(lambda book: get_time_delta(book.read_date).days < 30, new_books))

    for book in recent_new_books:
        print(book)

    if len(recent_new_books) == 0:
        continue

    message: Message = Message()

    if id in user_name_map:
        message.add_text(user_name_map[id])
    else:
        message.add_text(id)

    message.add_text("has finished reading")

    if len(recent_new_books) == 1:
        message.add_book(recent_new_books[0], end=".")
    elif len(recent_new_books) == 2:
        message.add_book(recent_new_books[0])
        message.add_text("and")
        message.add_book(recent_new_books[1])
    else:
        for book in recent_new_books[:-1]:
            message.add_book(book, end=", ")
        message.add_text("and")
        message.add_book(recent_new_books[-1], end=".")

    message.send()

    # Used to test different occurence repeatedly
    books_to_del = [
        # SimpleBook(title="Crooked Kingdom (Six of Crows, #2)", id="22299763", read_date=datetime(2025, 1, 12, 0, 0, tzinfo=timezone.utc)),
        # SimpleBook(title="Six of Crows (Six of Crows, #1)", id="23437156", read_date=datetime(2025, 1, 8, 0, 0, tzinfo=timezone.utc)),
    ]

    for b in books_to_del:
        if b in books:
            books.remove(b)

    save_user_history(id, books)
