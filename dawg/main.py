#!/usr/bin/env python3
from asyncio import get_event_loop
from typing import List
import sys

import server


def main(argv: List[str]):
    loop = get_event_loop()
    server.run_server(loop)


if __name__ == '__main__':
    main(sys.argv[1:])
