import xml.etree.ElementTree as ET

class xml2list(object):
  def __init__(self, classes):
    self.classes = classes
  
  def __call__(self, xml_path):
    ret = []
    xml = ET.parse(xml_path).getroot()
    
    for size in xml.iter("size"):
      width = float(size.find("width").text)
      height = float(size.find("height").text)
    
    for obj in xml.iter("object"):
      # 判断難しい画像はスキップ
      difficult = int(obj.find("difficult").text)
      if difficult == 1:
        continue
      
      bndbox = [width, height]
      
      name = obj.find("name").text.lower().strip() # 小文字にして空白削除
      bbox = obj.find("bndbox")
      
      pts = []
