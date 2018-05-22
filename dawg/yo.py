#!/usr/bin/env python3

from asyncio import get_event_loop
from typing import Optional, List
import sys

from aiohttp import ClientSession

from notifier import Notifier


def mk_yo_notifier(client_session: ClientSession, api_key: str) -> Notifier:
    async def yo_notify(username: str) -> Optional[Exception]:
        url = "http://localhost:8000/df.txt"
        async with client_session.get(url) as response:
            txt = await response.text()
            print(txt)
            return None
    return yo_notify


async def main(argv: List[str]) -> None:
    api_key = argv[0]
    async with ClientSession() as client_session:
        notifier = mk_yo_notifier(client_session, api_key)
        response = await notifier('dfbot')
        print(response)
        return None

if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(main(sys.argv))
