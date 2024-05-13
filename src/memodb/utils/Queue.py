import threading
import time
import datetime
import Singleton

class Queue:
  def __init__(self,wait_time = 5):
    self.q = []
    self.subscriptors = []
    self.lock = threading.Lock()
    self.__wait_time__ = wait_time
    self.start_worker();

  
  def suscribe(self, func):
    self.lock.acquire()
    self.subscriptors.append(func)
    self.lock.release()

  
  def add(self,data):
    self.lock.acquire()
    self.q.insert(0,data)
    self.lock.release()

  
  def __notify__(self):
    data = self.q.pop()
    for subs in self.subscriptors:
      subs(data)

  def start_worker(self):
    worker = threading.Thread(target=self.__worker__)
    worker.daemon = True
    worker.start()

  def __worker__(self):
    while True:
      if len(self.q) != 0:
        self.lock.acquire()
        self.__notify__()
        self.lock.release()
      else:
        time.sleep(self.__wait_time__)
    
  
class Error:
  def __init__(self,msg, timestamp = time.time()) -> None:
    self.msg = msg
    self.timestamp = timestamp


class ErrorQueue(Queue,metaclass=Singleton.SingletonMeta):
  def __init__(self) -> None:
    super().__init__(wait_time=1)
    super().suscribe(ErrorQueue.__print_error__)

  def add(self,msg):
    super().add(Error(msg))

  def __print_error__(error: Error):
    date = datetime.datetime.fromtimestamp(error.timestamp)
    print(f"[{date}]: {error.msg}")

  
  
