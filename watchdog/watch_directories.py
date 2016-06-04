from pathlib import Path
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler


class MyEventHandler(FileSystemEventHandler):
    def dispatch(self, evt):
        if not evt.is_directory:
            print('%s: %s' % (evt.event_type, evt.src_path))


if __name__ == '__main__':
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(
        event_handler, str(Path('.').parent / 'aiohttp'), recursive=True)
    observer.schedule(
        event_handler, str(Path('.').parent / 'tornado'), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
