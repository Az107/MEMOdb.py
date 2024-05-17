import importlib.util
from utils.Queue import ErrorQueue, Queue
from watchdog.observers import Observer
import time
import sys
import threading
import os


class masterNGN:
  front_module = None;
  modoules = []
  errorQ = ErrorQueue()
  qs: dict[str,Queue] = dict()

  def __load_module__(self,path: str):
    try:
      spec = importlib.util.spec_from_file_location("module", path)
      module = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(module)
    except Exception as E:
      self.errorQ.add(str(E),owner=path.split("/")[-1])
      module = None
    return module
  
  def add_queue(self,name:str):
     self.qs[name] = Queue()

  def __load_all__(self,path: str):
     suffix = "Engine.py"
     full_path = os.getcwd() + "/" + path;
     contents = os.listdir(full_path)
     for element in contents:
        if (element.endswith(suffix)):
          try:
            print(f"Loading {element.replace(suffix,"")}...",end="")
            m = self.__load_module__(full_path + element)
            if m is None:
               raise Exception("error importing")
            print("✅")
            if (hasattr(m,"Engine")):
               ngn = m.Engine
               if ngn.front:
                  try:
                    self.front_module = ngn(ctx=self)
                  except:
                     self.errorQ.add(str(E), element)
                  
               else:
                  try:
                    worker = threading.Thread(target=ngn(ctx=self).run)
                    worker.daemon = True
                    worker.start()
                  except Exception as E:
                      self.errorQ.add(str(E), element)
                      continue
                  self.modoules.append(worker)

          except Exception as E:
            print("❌\n\t" + str(E))  



  def __on_modified__(self,event):
     self.__load_module__
  
  def Worker(self, path):
    self.add_queue("_MASTER")
    observer = Observer()
    self.qs.get("_MASTER").suscribe(lambda msg: observer.stop())
    observer.schedule(self.__on_modified__, path, recursive=True)
    observer.start()
    try:
        while observer.is_alive():
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


  def NGNloader(self):
    # Start watchdog and reload each thread
    self.__load_all__("src/memodb/Engines/")
    t = threading.Thread(target=self.Worker,args=("src/memodb/Engines/",))
    t.daemon = True
    t.start()
    if self.front_module is not None:
       self.front_module.run()
    else: 
       print("Printing error traceback")
       for entry in self.errorQ.q:
           ErrorQueue.__print_error__(entry)
    self.qs.get("_MASTER").add("stop")
    print("Finishing tasks...",end="")
    t.join();
    print("OK")


class NGNbase:
   name = "base"
   front = False
   ctx = masterNGN | None
   
   def __init__(self,name: str | None = None ,ctx : masterNGN | None = None,front=False) -> None:
      self.ctx = ctx;
      self.front = front
      if name is not None: self.name = name

   def run():
      pass