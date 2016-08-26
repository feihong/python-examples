import asyncio
from aiohttp import web


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    print('Web socket opened')

    async for msg in ws:
        print(msg.data)

    print('Web socket closed')
    return ws


if __name__ == '__main__':
    app = web.Application()
    app.router.add_route('GET', '/websocket/', websocket_handler)
    web.run_app(app)
