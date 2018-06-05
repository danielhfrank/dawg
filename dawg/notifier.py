from enum import Enum, auto
from typing import Callable, Optional, Awaitable, NamedTuple


Notifier = Callable[[str, str], Awaitable[Optional[Exception]]]


class NotifierType(Enum):

    YO = auto()
    PUSHOVER = auto()


class APIToken(NamedTuple):
    notifier_type: NotifierType
    token: str


async def print_notifier(username: str, message: str) -> Optional[Exception]:
    print(f'{username}: {message}')
    return None
