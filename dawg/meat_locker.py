from typing import Dict, NamedTuple, NewType, Union, Optional

from notifier import Notifier, print_notifier


class NotificationRequest(NamedTuple):
    request_id: str
    username: str


Tombstone = NewType('Tombstone', int)


class MeatLocker(object):

    def __init__(self, ack_timeout: float) -> None:
        self.ack_timeout = ack_timeout
        self.locker: Dict[str, Union[NotificationRequest, Tombstone]] = {}
        self.notifier: Notifier = print_notifier

    def store(self, notification_request: NotificationRequest) -> bool:
        self.locker[notification_request.request_id] = notification_request
        self.maybe_fire(notification_request.request_id)
        return True
        # TODO syntax for calling fire later

    async def maybe_fire(self, request_id: str) -> bool:
        notification_request = self.locker[request_id]
        if isinstance(notification_request, NotificationRequest):
            result: Optional[Exception] = self.notifier(notification_request.username)
            return (result is None)
        else:
            return False

    def complete(self, request_id: str):
        pass
