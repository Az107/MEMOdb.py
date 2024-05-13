from utils.Queue import Queue
from Core import *
from NGN import NGNbase, masterNGN



class Engine(NGNbase):
  db = dict()
  selected = None
  front = True
  name = "Repl"

  def list_db(self):
    for d in self.db:
      print(f"-> {self.db[d].name}")

  def select(self,name):
    if self.db.get(name) is not None:
      print(f"Using {name}")
      self.selected = name
    else:
      print("Collection does not exist")
      self.ctx.errorQ.add("Collection does not exist",self.name)

  def createCollection(self,name):
    self.db[name] = Collection(name=name)

  Commands = {
    "echo": lambda self, args: print(" ".join(args)),
    "create": lambda self, args: self.createCollection(args[0]),
    "list": lambda self, args: self.list_db(),
    "select": lambda self, args: self.select(args[0]),
    "list_mod": lambda self, args: print(f"Modules: {len(self.ctx.modoules)}"),
    "list_qs": lambda self,args: print("->" + "\n->".join(self.ctx.qs)),
    "read_q": lambda self,args: print("\n".join(map(lambda item: str(item),self.ctx.qs[args[0]].q))),
    "exec": lambda self,args: exec(" ".join(args)),
    "help": lambda self, args: print("->" + "\n->".join(self.Commands))
  }
  
  def __init__(self, name: str | None = None, ctx: masterNGN | None = None, front=False) -> None:
    super().__init__(name, ctx, front)
    ctx.add_queue(self.name)
    self.stdout = Queue()
    self.db = dict()

  def run(self):
    while True:
      print(f"{self.selected or ""}> ",end="")
      cmd = input()
      if cmd == "": continue;
      self.ctx.qs[self.name].add(cmd)
      try:
        cmd,args = cmd.split(" ", 1)
        args = args.split()
      except:
        args = []
      if (cmd == "exit"): break
      try:
        self.Commands[cmd](self, args)
      except KeyError:
        print("Command not found")
      except Exception as E:
        self.ctx.errorQ.add(str(E),self.name)
        # print(f"Error: {E}")
