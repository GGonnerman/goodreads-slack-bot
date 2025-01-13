import requests
import os
from dotenv import load_dotenv
from simple_book import SimpleBook

load_dotenv()

slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")

goodreads_book_link_template = "https://www.goodreads.com/book/show/%s"


class Message:
    def __init__(self):
        self._headers: dict[str, str] = {"Content-Type": "application/json"}
        self._content: str = ""

    def set_headers(self, headers: dict[str, str]) -> None:
        self._headers = headers

    def add_text(self, text: str, end: str = " ") -> None:
        self._content += text + end

    def add_book(self, book: SimpleBook, end: str = " ") -> None:
        has_date = book.read_date is not None
        link = goodreads_book_link_template % book.id

        self.add_link(book.title, link, " " if has_date else end)

        if has_date:
            formatted_date = book.read_date.strftime("%A (%b %-d)")
            self.add_text(f"on {formatted_date}", end)

    def add_link(self, text: str, link: str, end: str = " ") -> None:
        cleaned_link = link.replace(" ", "%20")
        self._content += f"<{cleaned_link}|{text}>" + end

    def send(self) -> None:
        if slack_webhook_url is None:
            raise Exception("Cannot send message without valid slack_webhook_url. It should be provided in .env")

        json_data: dict[str, str] = {
            "text": self._content,
        }

        # print("Emulating slack channel...")
        # print(f"\t[Goodreader]: {self._content}")

        response: requests.Response = requests.post(url=slack_webhook_url, headers=self._headers, json=json_data)
        if response.status_code != 200:
            raise Exception(f"Recieved non-200 status code [{response.status_code}].")
