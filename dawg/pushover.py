#!/usr/bin/env python3

from asyncio import get_event_loop
from typing import Optional, List
import sys

from aiohttp import ClientSession

from notifier import Notifier


API_URL = 'https://api.pushover.net/1/messages.json'


def mk_pushover_notifier(client_session: ClientSession,
                         api_key: str) -> Notifier:
    async def pushover_notify(username: str) -> Optional[Exception]:
        post_data = {'user': username, 'token': api_key, 'message': 'yo dawg'}
        async with client_session.post(API_URL, data=post_data) as response:
            response_data = await response.json()
            print(response_data)
            return None
    return pushover_notify


async def main(argv: List[str]) -> None:
    api_key = argv[1]
    async with ClientSession() as client_session:
        notifier = mk_pushover_notifier(client_session, api_key)
        await notifier('uwszpfiid9bxqfwkc4d576nq1x5445')

if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(main(sys.argv))
