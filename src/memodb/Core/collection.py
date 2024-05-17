from .document import Document
from ..Server import Server
import uuid

class Collection:
  def __init__(self,name: str, server = None) -> None:
    self.name = name
    self.data = []
    self.id_table: [Document] = {}
    if server is not None: self.serv = server
  

  def add(self, document: Document):
    self.data.append(document)
    index = len(self.data) - 1
    self.id_table[document.ID] = index
    if hasattr(self, "serv"): self.serv.add_document(self.name, document)
    return index

  def _find(self, **args) -> [Document]:
    result = []
    for k in args:
      v = args[k]
      for doc in self.data:
        if doc.has(k,v):
          result.append(doc)
    return result

  def find(self, **args) -> [Document]:
    if hasattr(self, "serv"):
      return self.serv.find_document(self.name, **args)
    else:
      return self._find(args)

  def rm(self,d_id: uuid.UUID):
    index = self.id_table[d_id]
    self.data.pop(index)
    if hasattr(self, "serv"): self.serv.add_document(self.name, d_id)
    self.__indexTable__()

  def get(self,d_id: uuid.UUID):
    index = self.id_table.get(d_id)
    if (index == None and hasattr(self, "serv")):
       doc = self.serv.get_document(self.name, d_id)
       if (doc != None):
         self.data.append(doc)
         self.id_table[d_id] = len(self.data - 1)
         index = len(self.data - 1)
    return self.data[index]

  def __indexTable__(self):
    self.id_table = {}
    index = 0
    for document in self.data:
      self.id_table[document.ID] = index
      index+=1
  
