import asyncio
from pathlib import Path
from aiohttp import web, MsgType
from concurrent.futures import CancelledError


async def index(request):
    with (Path(__file__).parent / 'index.html').open('rb') as fp:
        return web.Response(body=fp.read())


async def websocket_handler(request):
    resp = web.WebSocketResponse()
    await resp.prepare(request)

    print('Someone joined.')

    request.app['sockets'].add(resp)

    task = asyncio.ensure_future(count(resp, 10))
    async for msg in resp:
        print(msg.data)

    if not task.done():
        task.cancel()

    await resp.close()

    print('Websocket connection closed')

    request.app['sockets'].remove(resp)
    return resp


async def count(ws, n):
    """
    Send 1 to n numbers to the given websocket.

    """
    for i in range(1, n+1):
        try:
            ws.send_str(str(i))
            await asyncio.sleep(1.0)
        except CancelledError:
            print('Count was cancelled at %d' % i)
            return 


def main():
    app = web.Application()
    app['sockets'] = set()
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/websocket/', websocket_handler)
    app.router.add_static('/static/', Path(__file__).parent)
    web.run_app(app)


if __name__ == '__main__':
    main()
