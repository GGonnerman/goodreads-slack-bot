from rss_parser.models import XMLBaseModel
from rss_parser.models.rss import RSS
from rss_parser.models.types.only_list import OnlyList
from rss_parser.models.types.tag import Tag
from rss_parser.pydantic_proxy import import_v1_pydantic

pydantic = import_v1_pydantic()


class BookSubitem(XMLBaseModel):
    num_pages: Tag[str] = pydantic.Field(alias="num_pages", default=None)


class BookItem(XMLBaseModel):
    guid: Tag[str] = pydantic.Field(alias="guid", default=None)
    pubDate: Tag[str] = pydantic.Field(alias="pubDate", default=None)
    title: Tag[str] = pydantic.Field(alias="title", default=None)
    link: Tag[str] = pydantic.Field(alias="link", default=None)
    book_id: Tag[str] = pydantic.Field(alias="book_id", default=None)
    book_image_url: Tag[str] = pydantic.Field(alias="book_image_url", default=None)
    book_small_image_url: Tag[str] = pydantic.Field(alias="book_small_image_url", default=None)
    book_medium_image_url: Tag[str] = pydantic.Field(alias="book_medium_image_url", default=None)
    book_large_image_url: Tag[str] = pydantic.Field(alias="book_large_image_url", default=None)
    book_description: Tag[str] = pydantic.Field(alias="book_description", default=None)
    author_name: Tag[str] = pydantic.Field(alias="author_name", default=None)
    isbn: Tag[str] = pydantic.Field(alias="isbn", default=None)
    user_name: Tag[str] = pydantic.Field(alias="user_name", default=None)
    user_rating: Tag[str] = pydantic.Field(alias="user_rating", default=None)
    user_read_at: Tag[str] = pydantic.Field(alias="user_read_at", default=None)
    user_date_added: Tag[str] = pydantic.Field(alias="user_date_added", default=None)
    user_date_created: Tag[str] = pydantic.Field(alias="user_date_created", default=None)
    user_shelves: Tag[str] = pydantic.Field(alias="user_shelves", default=None)
    user_review: Tag[str] = pydantic.Field(alias="user_review", default=None)
    average_rating: Tag[str] = pydantic.Field(alias="average_rating", default=None)
    book_published: Tag[str] = pydantic.Field(alias="book_published", default=None)
    description: Tag[str] = pydantic.Field(alias="description", default=None)
    book: Tag[BookSubitem] = pydantic.Field(alias="book", default=None)


class Channel(XMLBaseModel):
    items: OnlyList[Tag[BookItem]] = pydantic.Field(alias="item", default=[])


class BookRSS(XMLBaseModel):
    channel: Tag[Channel]
