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

  def rm(self, key: str):
    del self[key]
    return self
  
  def to_json(self) -> str:
     return json.dumps(self.__dict__)
    

