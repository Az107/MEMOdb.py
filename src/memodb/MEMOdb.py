from .Core import *
from Server import Server

class MEMOdb:
  collections = []
  server = None
  
  def __init__(self,url = None) -> None:
    if url is not None:
      self.server = Server(url)

  def create(self, name):
    Collection(name, self.server)
