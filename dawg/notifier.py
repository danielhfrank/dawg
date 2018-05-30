from enum import Enum, auto
from typing import Callable, Optional, Awaitable, NamedTuple


Notifier = Callable[[str], Awaitable[Optional[Exception]]]


class NotifierType(Enum):

    YO = auto()
    PUSHOVER = auto()


class APIToken(NamedTuple):
    notifier_type: NotifierType
    token: str


async def print_notifier(username: str) -> Optional[Exception]:
    print(username)
    return None
