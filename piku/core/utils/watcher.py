import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class EventHandler(PatternMatchingEventHandler):
    def __init__(self):
        super().__init__(ignore_directories=True, ignore_patterns=[
            '*.pytest_cache*',
            '*__pycache__*',
            '*.cache',
            '*.pyc'])
        self.changed = True

    def check(self, handler):
        if self.changed:
            self.changed = False
            handler()

    def on_any_event(self, event):
        self.changed = True

def watch(path, on_change):
    handler = EventHandler()
    observer = Observer()
    observer.schedule(handler, path, recursive=True)
    observer.start()
    try:
        while observer.is_alive():
            handler.check(on_change)
            observer.join(0.25)
            time.sleep(.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
