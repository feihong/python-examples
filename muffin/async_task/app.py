import json
import asyncio
import muffin
from muffin_example import ExampleApplication, WebSocketWriter


app = ExampleApplication()
app.register_static_resource()


@app.register('/websocket/')
async def websocket(request):
    ws = muffin.WebSocketResponse()
    await ws.prepare(request)
    print('Websocket opened')

    task = None

    async for msg in ws:
        print(msg)
        if msg.data == 'start' and not task:
            coroutine = long_task(WebSocketWriter(ws))
            task = asyncio.ensure_future(coroutine)
            def done(future):
                nonlocal task
                task = None
            task.add_done_callback(done)
        elif msg.data == 'stop' and task:
            task.cancel()
            task = None

    await ws.close()
    print('Websocket closed')

    return ws


async def long_task(writer):
    total = 150
    for i in range(1, total+1):
        writer.write(type='progress', value=i, total=total)
        await asyncio.sleep(0.05)
