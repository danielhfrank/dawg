#!/usr/bin/env python3

from asyncio import AbstractEventLoop

from aiohttp import web, ClientSession


async def handle(request: web.Request) -> web.Response:
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


class DawgServer(object):

    def __init__(self):
        self.session = ClientSession()

    async def fwd(self, request: web.Request) -> web.Response:
        fwd_path = request.match_info.get('fwd_path')
        url = 'http://localhost:8000/%s' % fwd_path
        client_resp = await self.session.get(url)
        client_resp_text = await client_resp.text()
        return web.Response(text=client_resp_text)

    def close(self):
        self.session.close()


async def prepare_app() -> web.Application:
    app = web.Application()
    server = DawgServer()

    app.add_routes([web.get('/', handle),
                    web.get('/{name}', handle),
                    web.get('/fwd/{fwd_path}', server.fwd)])
    return app


def run_server(loop: AbstractEventLoop):
    web.run_app(prepare_app())
