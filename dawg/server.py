#!/usr/bin/env python3

from asyncio import AbstractEventLoop

from aiohttp import web, ClientSession

from meat_locker import MeatLocker, NotificationRequest


class DawgServer(object):

    def __init__(self) -> None:
        self.session = ClientSession()
        self.meat_locker = MeatLocker(30.0)

    async def fwd(self, request: web.Request) -> web.Response:
        fwd_path = request.match_info.get('fwd_path')
        url = 'http://localhost:8000/%s' % fwd_path
        client_resp = await self.session.get(url)
        client_resp_text = await client_resp.text()
        return web.Response(text=client_resp_text)

    async def store(self, request):
        req_id = request.match_info.get('id')
        notification_request = NotificationRequest(req_id, 'df')
        await self.meat_locker.store(notification_request)
        return web.Response()


    def close(self):
        self.session.close()


async def prepare_app() -> web.Application:
    app = web.Application()
    server = DawgServer()

    app.add_routes([web.get('/fwd/{fwd_path}', server.fwd),
                    web.get('/store/{id}', server.store)])
    return app


def run_server(loop: AbstractEventLoop):
    web.run_app(prepare_app())
