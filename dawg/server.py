#!/usr/bin/env python3

from asyncio import AbstractEventLoop

from aiohttp import web, ClientSession

from meat_locker import MeatLocker, NotificationRequest


class DawgServer(object):

    def __init__(self, loop: AbstractEventLoop) -> None:
        self.session = ClientSession()
        self.meat_locker = MeatLocker(loop, 10.0)

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

    async def close(self, app):
        await self.session.close()


async def prepare_app(loop) -> web.Application:
    app = web.Application()
    server = DawgServer(loop=loop)

    app.add_routes([web.get('/arm/{id}', server.arm),
                    web.get('/ack/{id}', server.ack)])
    app.on_shutdown.append(server.close)
    return app


def run_server(loop: AbstractEventLoop):
    web.run_app(prepare_app(loop))
