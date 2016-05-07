import asyncio
from pathlib import Path
from aiohttp import web, MsgType


async def index(request):
    with (Path(__file__).parent / 'index.html').open('rb') as fp:
        return web.Response(body=fp.read())


async def websocket_handler(request):
    resp = web.WebSocketResponse()
    await resp.prepare(request)

    print('Someone joined.')

    request.app['sockets'].add(resp)

    for i in range(5):
        await asyncio.sleep(1.0)
        resp.send_str(str(i))

    await resp.close()

    print('Websocket connection closed')

    request.app['sockets'].remove(resp)
    return resp


def main():
    app = web.Application()
    app['sockets'] = set()
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/websocket/', websocket_handler)
    app.router.add_static('/static/', Path(__file__).parent)
    web.run_app(app)


if __name__ == '__main__':
    main()
