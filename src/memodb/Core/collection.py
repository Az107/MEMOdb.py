from .document import Document
from ..Engines import Server
import uuid

class Collection:
  def __init__(self,name: str, url = None) -> None:
    self.name = name
    self.data = []
    self.id_table: [Document] = {}
    if url != None: self.serv = Server(url)
  

  def add(self, document: Document):
    self.data.append(document)
    index = len(self.data) - 1
    self.id_table[document.ID] = index
    if hasattr(self, "serv"): self.serv.add_document(self.name, document)
    return index

  def rm(self,d_id: uuid.UUID):
    index = self.id_table[d_id]
    self.data.pop(index)
    if hasattr(self, "serv"): self.serv.add_document(self.name, d_id)
    self.__indexTable__()

  def get(self,d_id: uuid.UUID):
    index = self.id_table.get(d_id)
    if (index == None and hasattr(self, "serv")):
       doc = self.serv.get_document(d_id)
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
  
