import json
import asyncio
import threading
import muffin
from muffin_example import ExampleApplication, ThreadSafeWebSocketWriter


app = ExampleApplication()


@app.register('/websocket/')
async def websocket(request):
    ws = muffin.WebSocketResponse()
    await ws.prepare(request)
    print('Websocket opened')

    loop = asyncio.get_event_loop()
    stop_event = threading.Event()
    task = None
    def done(future):
        print('done!')
        nonlocal task
        task = None
        stop_event.clear()

    async for msg in ws:
        print(msg)
        if msg.data == 'start' and not task:
            coroutine = loop.run_in_executor(
                None, long_task, ThreadSafeWebSocketWriter(ws), stop_event)
            task = asyncio.ensure_future(coroutine)
            task.add_done_callback(done)
        elif msg.data == 'stop' and task:
            stop_event.set()

    await ws.close()
    print('Websocket closed')

    return ws


def long_task(writer, stop_event):
    import time

    total = 150
    for i in range(1, total+1):
        if stop_event.is_set():
            return
        writer.write(type='progress', value=i, total=total)
        time.sleep(0.05)
