import asyncio
import aiohttp


async def main():
    session = aiohttp.ClientSession()
    ws = await session.ws_connect('ws://localhost:8080/websocket/')
    for text in ['hello world', 'Hippy Barfday', 'l33t']:
        ws.send_str(text)
        msg = await ws.receive()
        print(msg.data)
    await ws.close()
    await session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
