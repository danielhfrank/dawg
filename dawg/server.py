#!/usr/bin/env python3

from asyncio import AbstractEventLoop
from typing import Optional

from aiohttp import web, ClientSession

from meat_locker import MeatLocker, NotificationRequest
from notifier import print_notifier, mk_yo_notifier, Notifier


class DawgServer(object):

    def __init__(self, loop: AbstractEventLoop, notifier: Notifier) -> None:
        self.meat_locker = MeatLocker(loop, 10.0, notifier)

    async def arm(self, request):
        req_id = request.match_info.get('id')
        username = request.query['username']
        notification_request = NotificationRequest(req_id, username)
        await self.meat_locker.arm(notification_request)
        return web.Response()

    async def ack(self, request):
        req_id = request.match_info.get('id')
        try:
            self.meat_locker.complete(req_id)
        except KeyError:
            raise web.HTTPNotFound()
        return web.Response(text=f"Acknowledged request {req_id}")


async def prepare_app(loop: AbstractEventLoop,
                      yo_api_key: Optional[str]) -> web.Application:
    app = web.Application()
    client_session = ClientSession()
    # TODO create notifier here
    if yo_api_key is not None:
        notifier = mk_yo_notifier(client_session, yo_api_key)
    else:
        notifier = print_notifier

    async def close(app):
        await client_session.close()
    server = DawgServer(loop=loop, notifier=notifier)

    app.add_routes([web.get('/arm/{id}', server.arm),
                    web.get('/ack/{id}', server.ack)])
    app.on_shutdown.append(close)
    return app


def run_server(loop: AbstractEventLoop, api_key: Optional[str]) -> None:
    web.run_app(prepare_app(loop, api_key))
