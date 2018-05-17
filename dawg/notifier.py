from typing import AsyncGenerator, Optional

Notifier = AsyncGenerator[Optional[Exception], str]


async def print_notifier(username: str) -> Optional[Exception]:
    print(username)
    return None
