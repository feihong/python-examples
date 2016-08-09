import json
import asyncio
import muffin
from muffin_example import ExampleApplication, ThreadSafeWebSocketWriter


app = ExampleApplication()


@app.register('/websocket/')
async def websocket(request):
    ws = muffin.WebSocketResponse()
    await ws.prepare(request)
    print('Websocket opened')

    loop = asyncio.get_event_loop()
    task = None

    async for msg in ws:
        print(msg)
        if msg.data == 'start' and not task:
            coroutine = loop.run_in_executor(None, long_task, ThreadSafeWebSocketWriter(ws))
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


def long_task(writer):
    import time

    total = 150
    for i in range(1, total+1):
        writer.write(type='progress', value=i, total=total)
        time.sleep(0.05)
