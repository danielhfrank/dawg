#!/usr/bin/env python3
from asyncio import get_event_loop
from argparse import ArgumentParser
from typing import List
import sys

from dawg.notifier import APIToken, NotifierType
import dawg.server as server


def main(argv: List[str]):
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--test', action='store_true',
                       help='Just print username')
    group.add_argument('--yo-api-token')
    group.add_argument('--pushover-api-token')
    args = parser.parse_args()
    loop = get_event_loop()
    api_token = None
    if args.yo_api_token:
        api_token = APIToken(NotifierType.YO, args.yo_api_token)
    elif args.pushover_api_token:
        api_token = APIToken(NotifierType.PUSHOVER, args.pushover_api_token)
    server.run_server(loop, api_token)


if __name__ == '__main__':
    main(sys.argv[1:])
