from functools import cache
from ..Core import *
import requests
import json


class Server:
  def __init__(self,url: str) -> None:
    self.url = url
    try:
      if not requests.get(url=url).ok:
        raise Exception("unable to connect")
    except:
        raise Exception("unable to connect")


  def cache_clear(self):
    self.list_collections.cache_clear()
    self.get_all_documents.cache_clear()
    self.get_document.cache_clear()


  @cache 
  def list_collections(self) -> list:
    collections = requests.get(url=self.url).json()
    return collections
  
  @cache 
  def get_all_documents(self,collection_name) -> list:
    url = f"{self.url}{collection_name}/all"
    response = requests.get(url=url)
    if response.ok:
      doc_list = []
      raw_list = response.json()
      for raw in raw_list:
        doc = Document(json.dumps(raw))
        doc_list.append(doc)
      return doc_list

  @cache 
  def get_document(self,collection_name,ID):
    url = f"{self.url}{collection_name}/{ID}"
    response = requests.get(url=url)
    if response.ok:
      return Document(response.json())
    
  
  def update_document(self, collection_name,ID,diff):
    url = f"{self.url}{collection_name}/{ID}"
    response = requests.put(url,json=diff)
    if response.ok:
      self.get_document.cache_clear()
      self.get_all_documents.cache_clear() 
      return response.text  

  def find_document(self,collection_name,**params):
    url_base = f"{self.url}{collection_name}/find?"
    for k in params:
      v = params[k]
      url_base + f"{k}={v}&"
    url = url_base.rstrip('&')
    response = requests.get(url)
    if response.ok:
      doc_list = []
      raw_list = response.json()
      for raw in raw_list:
        doc = Document(json.dumps(raw))
        doc_list.append(doc)
      return doc_list

    
  
  def add_document(self,collection_name,document: Document):
    url = f"{self.url}{collection_name}/_"
    response = requests.post(url,data=document.to_json())
    if response.ok:
      self.get_document.cache_clear()
      self.get_all_documents.cache_clear() 
      return response.text

  def del_document(self,collection_name,ID):
    url = f"{self.url}{collection_name}/{ID}"
    response = requests.delete(url)
    if response.ok:
      return response.text
  
  

