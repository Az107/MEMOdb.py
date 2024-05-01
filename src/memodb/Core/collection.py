from .document import Document
import uuid

class Collection:
  def __init__(self,name: str) -> None:
    self.name = name
    self.data = []
    self.id_table: [Document] = {}
  

  def add(self, document: Document):
    self.data.append(document)
    index = len(self.data) - 1
    self.id_table[document.ID] = index
    return index

  def rm(self,id: uuid.UUID):
    index = self.id_table[uuid]
    self.data.pop(index)
    self.__indexTable__()

  def get(self,id: uuid.UUID):
    index = self.id_table[uuid]
    return self.data[index]

  def __indexTable__(self):
    self.id_table = {}
    index = 0
    for document in self.data:
      self.id_table[document.ID] = index
      index+=1
  
