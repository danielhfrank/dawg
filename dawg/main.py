#!/usr/bin/env python3
from asyncio import get_event_loop
from argparse import ArgumentParser
from typing import List
import sys

import server


def main(argv: List[str]):
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--test', action='store_true', help='Just print username')
    group.add_argument('--yo-api-key')
    args = parser.parse_args()
    loop = get_event_loop()
    server.run_server(loop, args.yo_api_key)


if __name__ == '__main__':
    main(sys.argv[1:])
