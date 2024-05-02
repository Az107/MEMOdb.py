# from src.memodb.Core import Collection, Document
import pytest
from src.memodb.Core import Collection, Document


def test_creation():
  collection = Collection(name="users")
  assert collection.name == "users"

def test_add():
  collection = Collection(name="users")
  document = Document('{"name": "Alb"}')
  collection.add(document)
  assert len(collection.data) == 1




  
