from typing import Callable, Optional, Awaitable

Notifier = Callable[[str], Awaitable[Optional[Exception]]]


async def print_notifier(username: str) -> Optional[Exception]:
    print(username)
    return None
