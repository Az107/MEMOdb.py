import importlib.util
from utils.Queue import ErrorQueue
from watchdog.observers import Observer
import time
import sys
import threading
import os


class masterNGN:
  mdoules = []
  errorQ = ErrorQueue()

  def __load_module__(self,path: str):
    try:
      spec = importlib.util.spec_from_file_location("module", path)
      module = importlib.util.module_from_spec(spec)
    except Exception as E:
      self.errorQ.add(str(E))
      module = None
    return module

  def Worker(path):
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


  def NGNloader():
    # Start watchdog and reload each thread
    pass
