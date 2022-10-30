from PIL import Image
import pyocr
# import pyocr.builders
pyocr.tesseract.TESSERACT_CMD = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' #これ入れないと動かないっぽい(デバッグ10/13)
# pyocr.tesseract.TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe"


# OCRエンジンを取得
engines = pyocr.get_available_tools()

engine = engines[0]

dirname= 'idake.png'
# 画像の文字を読み込む

txt = engine.image_to_string(Image.open(dirname), lang="jpn", builder=pyocr.builders.TextBuilder(tesseract_layout=10))
print(txt) # 「Test Message」が出力される