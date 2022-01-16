###########################################################
# 1. 画像ファイルのパスとXMLファイルのパスを取得する
###########################################################
from pathlib import Path

target_folder_img = "./privateDataset/img"
folder_path_img = Path(target_folder_img)
image_list = list(folder_path_img.glob('*.jpg'))

target_folder_xml = "./privateDataset/xml"
folder_path_xml = Path(target_folder_xml)
xml_list = list(folder_path_xml.glob('*.xml'))


###########################################################
# 2. お互いのファイル名が一致しているかをチェックする
###########################################################
for img, xml in zip(image_list,xml_list):
  if str(img)[-6:-4] != str(xml)[-6:-4]:
    print("ファイル名チェックNG")
    exit()
print("ファイル名チェックOK")


###########################################################
# 3. 一致してたら画像をリサイズして新しいフォルダに格納
###########################################################
import cv2

# for image in image_list:
#   image_name = str(image)[-6:-4]
#   img = cv2.imread(str(image))
#   # 800 600（HWが耐えられる範囲で大きい方がいい）
#   dst = cv2.resize(img, dsize=(800, 600))
#   print(f"{img.shape} -> {dst.shape}")
#   # cv2.imshow('image',dst)
#   # cv2.waitKey(0)
#   cv2.imwrite("./resize/img/"+f"{image_name}.jpg",dst)


###########################################################
# 4. 一致してたらXMLファイルを書き換えて新しいフォルダに格納
###########################################################
import xml.etree.ElementTree as ET

for xml in xml_list:
  xml_name = str(xml)[-6:-4]
  #xmlデータを読み込みます
  tree = ET.parse(str(xml))
  #一番上の階層の要素を取り出します
  root = tree.getroot()
  for child in root:
    if child.tag == "path":
      child.text = f"C:/Users/junichi doi/Documents/14_アノテーションツール/resize/img/{xml_name}.jpg"
    if child.tag == "size":
      original_width = child.find("width").text
      original_height = child.find("height").text
      child.find("width").text = "800"
      child.find("height").text = "600"
    if child.tag == "object":
      child.find("bndbox").find("xmin").text = str(int(int(child.find("bndbox").find("xmin").text)*(800/int(original_width))))
      child.find("bndbox").find("ymin").text = str(int(int(child.find("bndbox").find("ymin").text)*(600/int(original_height))))
      child.find("bndbox").find("xmax").text = str(int(int(child.find("bndbox").find("xmax").text)*(800/int(original_width))))
      child.find("bndbox").find("ymax").text = str(int(int(child.find("bndbox").find("ymax").text)*(600/int(original_height))))
  # 保存
  tree.write("./resize/xml/"+f"{xml_name}.xml")