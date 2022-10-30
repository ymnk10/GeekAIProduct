import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import cv2 #pipでもインストールしたら解決

# root = "https://www.perfume-web.jp/"
# url = "https://www.perfume-web.jp/index-jpn.php"
root = "http://127.0.0.1:8000/"
url = "http://127.0.0.1:8000/index2"
# store_path = "C:\\Users\\ymnk1\\GeekSalon\\beautifulsoup"
store_path = "C:\\Users\\ymnk1\\GeekSalon\\OCR2\\pafumepic.png" #\は二つ！！

def img_store(path):
    img = requests.get(path).content

    print(path)

    with open(store_path, "wb") as f:
        f.write(img)

    img_local = cv2.cvtColor(cv2.imread(store_path), cv2.COLOR_BGR2RGB)

    plt.imshow(img_local)
    plt.show()

for i in range(3):
    store_path = "C:\\Users\\ymnk1\\GeekSalon\\OCR2\\pic_number{}.png".format(i) 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    top_img2 = soup.find("div", class_="c-goods__thumbnail").find("img").get("src") #classを指定するときは「class_」で表すことに注意！！
    print(top_img2)
    img_url=root+top_img2 #img_urlは実際に写真自体をパスに指定しなければならない(フォルダじゃない！！)
    img_store(root+top_img2)



response = requests.get(url)
soup = BeautifulSoup(open('templates/index2.html', encoding="utf-8"), "html.parser") #書式を指定しないとUnicodeDecodeErrorになる
# soup = BeautifulSoup(url, "html.parser")
print(soup)
top_img2 = soup.find("div", id="bs").find("img", id="copyImg").get("src") #classを指定するときは「class_」で表すことに注意！！
print(top_img2)
img_url=root+top_img2 #img_urlは実際に写真自体をパスに指定しなければならない(フォルダじゃない！！)
img_store(root+top_img2)


# find("div", id="bs").