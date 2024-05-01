from src.memodb.Core import Document


def test_creation():
  doc = Document()
  assert doc.ID != None


def test_creation_with_data():
  doc = Document('{"name": "Alb"}')
  assert doc.name == "Alb"
  assert doc.ID != None
