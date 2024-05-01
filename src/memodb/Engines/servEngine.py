from ..Core import *
import requests


class Server:
  def __init__(self,url: str) -> None:
    self.url = url
    try:
      if not requests.get(url=url).ok:
        raise Exception("unable to connect")
    except:
        raise Exception("unable to connect")


  def list_collections(self) -> list:
    collections = requests.get(url=self.url).json
    return collections

