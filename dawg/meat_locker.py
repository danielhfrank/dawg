from asyncio import AbstractEventLoop, ensure_future
from typing import Dict, NamedTuple, NewType, Union, Optional

from notifier import Notifier


class NotificationRequest(NamedTuple):
    request_id: str
    username: str


Tombstone = NewType('Tombstone', int)


class MeatLocker(object):

    def __init__(self,
                 loop: AbstractEventLoop,
                 ack_timeout: float,
                 notifier: Notifier) -> None:

        self.loop = loop
        self.ack_timeout = ack_timeout
        self.locker: Dict[str, Union[NotificationRequest, Tombstone]] = {}
        self.notifier: Notifier = notifier

    async def arm(self, notification_request: NotificationRequest) -> None:
        self.locker[notification_request.request_id] = notification_request

        def fire_future():
            ensure_future(self.maybe_fire(notification_request.request_id))
        self.loop.call_later(self.ack_timeout, fire_future)

    async def maybe_fire(self, request_id: str) -> bool:
        notification_request = self.locker.pop(request_id)
        if isinstance(notification_request, NotificationRequest):
            result: Optional[Exception] = await \
                self.notifier(notification_request.username)
            return (result is None)
        else:
            return False

    def complete(self, request_id: str):
        self.locker.pop(request_id)
        self.locker[request_id] = Tombstone(0)
