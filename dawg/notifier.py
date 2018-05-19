from typing import Callable, Optional, Awaitable

from aiohttp import ClientSession

Notifier = Callable[[str], Awaitable[Optional[Exception]]]


async def print_notifier(username: str) -> Optional[Exception]:
    print(username)
    return None


def mk_yo_notifier(client_session: ClientSession, api_key: str) -> Notifier:
    async def yo_notify(username: str) -> Optional[Exception]:
        url = "http://localhost:8000/df.txt"
        async with client_session.get(url) as response:
            return None
    return yo_notify
