#!/usr/bin/env python3
from typing import List
import sys

import server


def main(argv: List[str]):
    server.run_server()


if __name__ == '__main__':
    main(sys.argv[1:])
