import sys
import time

from websocketclient import WebSocketClient


def long_task(url):
    with WebSocketClient(url) as client:
        total = 15
        for i in range(1, total+1):
            print(i)
            client.write(type='progress', value=i, total=total)
            time.sleep(0.05)


if __name__ == '__main__':
    long_task('ws://localhost:8080/websocket/')
