#!/usr/bin/env python3

from asyncio import AbstractEventLoop
import os
from typing import Optional

from aiohttp import web, ClientSession

from meat_locker import MeatLocker, NotificationRequest
from notifier import print_notifier, Notifier, APIToken, NotifierType
from yo import mk_yo_notifier
from pushover import mk_pushover_notifier


class DawgServer(object):

    def __init__(self, loop: AbstractEventLoop, notifier: Notifier) -> None:
        self.meat_locker = MeatLocker(loop, 10.0, notifier)

    async def arm(self, request):
        req_id = request.match_info.get('id')
        username = request.query['username']
        message = request.query.get('message', 'yo dawg')
        notification_request = NotificationRequest(req_id, username, message)
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
                      api_token: Optional[APIToken]) -> web.Application:
    app = web.Application()
    client_session = ClientSession()
    if api_token is not None:
        if api_token.notifier_type is NotifierType.YO:
            notifier = mk_yo_notifier(client_session, api_token.token)
        else:
            notifier = mk_pushover_notifier(client_session, api_token.token)
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
    port = os.environ.get('PORT')
    web.run_app(prepare_app(loop, api_key), port=port)
