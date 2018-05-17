#!/usr/bin/env python3

from aiohttp import web


async def handle(request: web.Request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


def run_server():
    app = web.Application()
    app.add_routes([web.get('/', handle),
                    web.get('/{name}', handle)])

    web.run_app(app)
