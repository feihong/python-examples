"""
This web app starts a counter task that counts from 1 to n (as specified by a
query string parameter). As it runs, the counter task sends a message to every
active websocket.

"""

import asyncio
from pathlib import Path
from aiohttp import web, MsgType
from concurrent.futures import CancelledError


async def index(request):
    app = request.app
    stop_num = int(request.GET.get('count', 10))
    if app['count_task'] is None or app['count_task'].done():
        print('Counting to %d' % stop_num)
        app['count_task'] = asyncio.ensure_future(count(app, stop_num))

    with (Path(__file__).parent / 'index.html').open('rb') as fp:
        return web.Response(body=fp.read())


async def websocket_handler(request):
    resp = web.WebSocketResponse()
    await resp.prepare(request)

    print('Someone joined.')

    request.app['sockets'].add(resp)

    async for msg in resp:
        print(msg.data)

    await resp.close()

    print('Websocket connection closed')

    request.app['sockets'].remove(resp)
    return resp


async def count(app, n):
    """
    Send 1 to n numbers to all websockets with a 1 second delay.

    """
    for i in range(1, n+1):
        print('Count: %d' % i)
        await asyncio.sleep(1.0)
        for ws in app['sockets']:
            ws.send_str(str(i))


def main():
    app = web.Application()
    app['sockets'] = set()
    app['count_task'] = None
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/websocket/', websocket_handler)
    app.router.add_static('/static/', Path(__file__).parent)
    web.run_app(app)


if __name__ == '__main__':
    main()
