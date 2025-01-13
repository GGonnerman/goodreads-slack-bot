from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SimpleBook:
    title: str
    id: str
    read_date: datetime | None
