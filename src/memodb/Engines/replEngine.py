from ..utils.Queue import ErrorQueue
from ..Core import *

errorQ = ErrorQueue()
db = []
selected = None

def list_db():
  for d in db:
    print(f"-> {d.name}")

def select(name):
  print(f"Using {name}")
  selected = name


Commands = {
  "echo": lambda args: print(" ".join(args)),
  "create": lambda args: db.append(Collection(args[0])),
  "list": lambda args: list_db(),
  "select": lambda args: select(args[0])
}


def repl():
  while True:
    print(f"{selected or ""}> ",end="")
    cmd = input()
    if cmd == "": continue;
    try:
      cmd,args = cmd.split(" ", 1)
      args = args.split()
    except:
      args = []
    if (cmd == "exit"): break
    try:
      Commands[cmd](args)
    except KeyError:
      print("Command not found")
    except  Exception as E:
      print(f"Error: {E}")
