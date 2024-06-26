import copy
import uuid
import json

class Document:
  def __setitem__(self, key, value):
      setattr(self, key, value)

  def __getitem__(self, key):
      return getattr(self, key)
  
  def __init__(self,data: str = "") -> None:
    if data != "":
       decoded_data = json.loads(data)
       for attr, value in decoded_data.items():
        self[attr] = value
    if not hasattr(self,"ID"): self.ID = uuid.uuid4()

  def add(self,key: str,value):
    self[key] = value
    return self
  
  def has(self,k: str,v):
     if hasattr(self,k):
        return self[k] == v
     return False

  def rm(self, key: str):
    del self[key]
    return self
  
  def to_json(self) -> str:
     doc_copy = copy.deepcopy(self)
     doc_copy.ID = str(doc_copy.ID)
     return json.dumps(doc_copy.__dict__,skipkeys=True)
  
  def __str__(self) -> str:
     return self.to_json()
  
  def __repr__(self) -> str:
     return self.to_json()
    

