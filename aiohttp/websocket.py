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

    async for msg in resp:
        if msg.tp == MsgType.text:
            if msg.data == 'stop':
                await resp.close()
            else:
                print('Received message: %s' % msg.data)
                resp.send_str('hello')
        elif msg.tp == MsgType.error:
            print('Websocket connection closed with exception %s' %
                resp.exception())

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
