import json
import asyncio
import threading
import muffin
from muffin_example import ExampleApplication, WebSocketWriter


app = ExampleApplication()


@app.register('/')
async def index(request):
    resp = muffin.StreamResponse()
    await resp.prepare(request)
    results = await fetch(1)
    resp.write(app.render('index.plim', results=results).encode('utf-8'))
    return resp


@app.register('/websocket/')
async def websocket(request):
    ws = muffin.WebSocketResponse()
    await ws.prepare(request)
    print('Websocket opened')

    writer = WebSocketWriter(ws)

    page = 2
    while not ws.closed:
        results = await fetch(page)
        if results is None:
            break
        writer.write(type='results', value=results)
        page += 1

    await ws.close()
    print('Websocket closed')

    return ws


app.register_static_resource()


async def fetch(page):
    if page >= 11:
        return None

    increment = 5
    start = (page - 1) * increment + 1
    end = start + increment
    await asyncio.sleep(1)
    return [i for i in range(start, end)]
