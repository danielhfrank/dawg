#!/usr/bin/env python3

from asyncio import get_event_loop
from typing import Optional, List
import sys

from aiohttp import ClientSession

from dawg.notifier import Notifier


YO_URL = 'https://api.justyo.co/yo/'


def mk_yo_notifier(client_session: ClientSession, api_key: str) -> Notifier:
    async def yo_notify(username: str) -> Optional[Exception]:
        post_data = {'username': username, 'api_token': api_key}
        async with client_session.post(YO_URL, data=post_data) as response:
            response_data = await response.json()
            print(response_data)
            return None
    return yo_notify


async def main(argv: List[str]) -> None:
    api_key = argv[1]
    async with ClientSession() as client_session:
        notifier = mk_yo_notifier(client_session, api_key)
        await notifier('dfbot')

if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(main(sys.argv))
