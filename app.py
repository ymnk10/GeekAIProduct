#!/bin/sh
# from flaskr import app
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import pyocr
# import base64
# import requests
# from bs4 import BeautifulSoup
# import numpy as np
# import io
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import cv2 #pipでもインストールしたら解決
import os

pyocr.tesseract.TESSERACT_CMD = 'Tesseract-OCR/tesseract.exe'
#これ入れないと動かないっぽい(デバッグ10/13)
# db.create_zyukugo_table()
# db.create_characters_table()
# DATABASE = 'database.db'

# app = Flask(__name__)
app = Flask(__name__, static_folder='static')


zyukugos = ['いちいたいすい','けんばのろう','ようとうくにく', 'けいめいくとう', 'せっさたくま', 'たざんのいし', 'いちいせんしん', 'りゅうりゅうしんく', 'ぼうじゃくぶじん', 'こううんりゅうすい',
 'いしんでんしん', 'ぶんしつひんぴん', 'おんこちしん', 'いっせきにちょう', 'にりつはいはん', 'ちょうさんぼし', 'ちょうれいぼかい', 'なんせんほくば', 'ごえつどうしゅう', 'がしんしょうたん',
 'せいしのひそみ', 'めいぼうこうし', 'しめんそか', 'ばつざんがいせい', 'けんどちょうらい', 'えいようえいが', 'きんかいっちょう', 'もんぜんじゃくら', 'けんこんいってき', 'せんゆうこうらく',
 'ふわらいどう', 'たいきばんせい', 'せつあんけいそう', 'せいこううどく', 'こうげんれいしょく', 'くんしひょうへん', 'にそくさんもん', 'さんみいったい', 'せいてんのへきれき', 'ぜんじんみとう',
 'ぎょふのり', 'てんちょうちきゅう', 'ひよくれんり', 'ごうほうらいらく', 'しょうしんよくよく', 'しゅんぷうたいとう', 'てんしんらんまん', 'ぎょくせきこんこう', 'せんざいいちぐう', 'なんざんのじゅ',
 'がりょうてんせい', 'めいそうじょうき', 'もうぼだんき', 'てんいむほう','たいざんほくと', 'とうりまんもん', 'りゅうあんかめい', 'さんしすいめい', 'こうりょういっすい', 'そっせんすいはん',
 'ひんこうほうせい', 'せいれんけっぱく', 'きょくすいりゅうしょう', 'さんかんしおん', 'しかいけいてい', 'ぜんとようよう', 'りっしんしゅっせ', 'せいうんのこころざし', 'けいこうぎゅうご', 'せいれいかっきん',
 'じがじさん', 'がでんいんすい', 'せんがくひさい', 'わこうどうじん', 'しゅしゅたいと', 'さいおうが の うま', 'そうせきちんりゅう', 'とういそくみょう', 'りんきおうへん', 'ちゃえんびんし',
 'こうふうせいげつ', 'やろうじだい', 'こふくげきじょう', 'どかいさんとう', 'しゅちにくりん', 'あくぎゃくむどう', 'こうとうむけい', 'しぶんごれつ', 'ごりむちゅう', 'じぼうじき',
 'くんしさんらく', 'めんもくやくじょ', 'こくしむそう', 'そうぎょうしゅせい', 'にしきをきてきょうにかえる', 'ごふうじゅう', 'いきようよう', 'ちょくじょうけいこう', 'きどあいらく', 'ひゃくかそうめい',
 'ひゃくかりょうらん', 'こうざんりゅうすい', 'かんぽうのまじわり', 'ふんけいのまじわり', 'たんとうちょくにゅう', 'げっかひょうじん', 'でんこうせっか', 'さんこうすいちょう', 'えんぼくきゅうぎょ', 'きんかぎょくじょう',
 'ふてんそっと', 'そうでんへきかい', 'きょうてんどうち', 'ごぞうろっぷ', 'ろっこんしょうじょう', 'けいこくけいせい', 'ちんぎょらくがん', 'きゅうそねこをかむ', 'かんぎゅうじゅうとう', 'こしたんたん', 'うとそうそう', 'がりょうほうすう', 'さんこのれい', 'がだてんそく', 'ばじとうふう',
 'たきぼうよう', 'ろうちょうかんえん', 'げんけいはくぞく', 'けいぐんのいっかく', 'せいがんはくがん', 'そうかのいぬ', 'ちょとつもうしん', 'こくしゅうきゅうけん', 'せっしやくわん', 'わこんかんさい',
 'いいだくだく', 'どんしゅうのうお', 'はいすいのじん', 'ひゃくしゃくかんとう', 'くうちゅうのろうかく', 'しちほのさい', 'かっかそうよう', 'ごんごどうだん', 'せんせんきょうきょう', 'こうせいおそるべし',
 'かんこつだったい', 'こうぜんのき', 'きんきじゃくやく', 'けいきゅうひば', 'かいろうどうけつ', 'きんしつあいわす', 'ふうじゅのたん', 'けんぼうじゅつすう', 'けんにんふばつ', 'しゅつらんのほまれ',
 'ちょううんぼう', 'がっしょうれんこう', 'ごかのあもう', 'ごぎゅうつきにあえぐ', 'りゅうかんりんり', 'しんとうめっきゃく', 'かろとうせん', 'なんかいちむ', 'こちゅうのてん', 'しちてんばっとう',
 'はっぽうびじん', 'びじんはくめい', 'いちじつのちょう', 'いちもうだじん', 'てんもうかいかい', 'てんばこうくう', 'ろかいじゅんこう', 'せいふうめいげつ', 'うかとうせん', 'はいばんろうぜき',
 'ぶんぶりょうどう', 'ぼうぜんじしつ', 'きしかいせい', 'ききゅうそんぼう', 'ききいっぱつ', 'せいせいどうどう', 'こうめいせいだい', 'かんたんあいてらす', 'たたますますべんず', 'じごうじとく',
 'いんがおうほう', 'てんばつてきめん', 'すいぎょのまじわり', 'きょくがくあせい', 'じゃくにくきょうしょく', 'ぜったいぜつめい', 'きゅうしいっしょう', 'りゅうげんひご', 'せいていのあ', 'しょくけんはいじつ',
 'ちみもうりょう', 'ようかいへんげ', 'ぜんどりゅうろう', 'きかおくべし', 'ゆうじゅうふだん', 'ゆうゆうじてき', 'さんさんごご', 'とうざんこうが', 'かんうんやかく', 'かくはつけいひ',
 'こうはつすいちょう', 'いもんのぼう', 'はんぽのこころ', 'やうたいしょう', 'こううんいじゅ', 'じょうじゅうざが', 'とうほんせいそう', 'しんしゅつきぼつ', 'ゆうおうまいしん', 'おうこうかっぽ',
 'ちょうりょうばっこ', 'じゅうようきゅうぼく', 'はんぶんじょくれい', 'きくじゅんじょう', 'しりめつれつ', 'ういてんぺん', 'えいこせいすい', 'こくくべんれい', 'ふんこつさいしん', 'うよきょくせつ',
 'しょしかんてつ', 'くうぜんぜつご', 'もうぼさんせん', 'ひっぷのゆう', 'ごうきぼくとつ', 'しつじつごうけん', 'きょしんたんかい', 'こうへいむし', 'せいてんはくじつ', 'しゅうそうれつじつ',
 'ぜぜひひ', 'むよくてんたん', 'しそうけんご', 'おんこうとくじつ', 'ききゅうのぎょう', 'めんもくやくじょ', 'しのうこうしょう', 'いっちはんかい', 'どくしょひゃっぺん', 'どくしょさんよ',
 'だんろんふうはつ', 'ないゆうがいかん', 'いんじゅんこそく', 'せきにんてんか', 'しんしょうひつばつ', 'かしのへき たま', 'さんぱつききょ', 'ほうとうこうめん', 'へいいはぼう', 'ほうかこうぎん',
 'ひふんこうがい', 'きそくえんえん', 'あいまいもこ', 'ふとくようりょう', 'かんかんがくがく', 'けんけんごうごう', 'むがむちゅう', 'うこさべん', 'とうこうきつりょく', 'はくさせいしょう',
 'ちょうていきょくほ', 'せいこううき', 'さんようすいたい', 'ふうこうめいび', 'しょうはくごちょう', 'しんしほしゃ', 'はほろびてしたそんす', 'いちびょうそくさい', 'ほりゅうのしつ', 'ようぼうかいい',
 'じんぴんこつがら', 'ふくとくえんまん', 'ふろうちょうじゅ', 'こうがんむち', 'しゅっしょしんたい', 'えこひいき', 'いっしどうじん', 'どくだんせんこう', 'しゅうしょうろうばい', 'いちようらいふく',
 'じゅんぷうまんぱん', 'ぼうねんのこう', 'こぎしゅんじゅん', 'しゅそりょうたん', 'じゅうねんいちじつ', 'いちじつせんしゅう', 'しっぷうもくう', 'たいあんきちじつ', 'らんびのさけ', 'そうこうのつま',
 'いっかだんらん', 'だんいほうしょく', 'かんこんそうさい', 'ろうしょうふじょう', 'せんしゅうばんざい', 'しょぎょうむじょう', 'しんちんたいしゃ', 'いちれんたくしょう', 'ふうりんかざん', 'せんぐんばんば',
 'いっきとうせん', 'しんぼうえんりょ', 'えんこうきんこう', 'ろんこうこうしょう', 'びもくしゅうれい', 'きんこつりゅうりゅう', 'おんじゅうとんこう', 'けいちょうふはく', 'としゅくうけん', 'ぼうこひょうが',
 'ししふんじん', 'はらんばんじょう', 'らくげつおくりょう', 'こりつむえん', 'てんがいこどく', 'こえいしょうぜん', 'ふとうふくつ', 'ちそくあんぶん', 'しゅうしんせいか', 'かくぶつちち',
 'じつじきゅうぜ', 'けいせいさいみん', 'りんげんあせのごとし', 'しもしたにおよばず', 'がんめいころう', 'ぜんしゃのてつ', 'いんかんとおからず', 'めんじゅうふくはい', 'ごうがんふそん', 'たしせいせい',
 'よゆうしゃくしゃく', 'じきゅうじそく', 'どうびょうあいあわれむ', 'きゅうぎゅうのいちもう', 'こくさくのきよう', 'ゆうめいむじつ', 'ろうきふくれき', 'どばじゅうが', 'がんこうしはい', 'いへんさんぜつ',
 'どくしょさんとう', 'だんしょうしゅぎ', 'だんかんれいぼく', 'ぶんじんぼっかく', 'きいんせいどう', 'じんめんとうか', 'じんめんじゅうしん', 'げいいんばしょく', 'すいせいむし', 'せんしゃくていしょう',
 'どうこういきょく', 'いきとうごう', 'ばくぎゃくのとも', 'そうじょうのじん', 'こうさんこうしん', 'ぜんだいみもん', 'ふえきりゅうこう', 'ぼくとつふけん', 'きんせいぎょくしん', 'へんげんせきご', 'いっちょういっせき', 'いちごいちえ']

characters = []

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/index2')
# def index2():
#     con = sqlite3.connect(DATABASE)
#     db_zyukugo = con.execute('SELECT * FROM zyukugo LIMIT 1').fetchall()
#     con.close()
#     zyukugo = []
#     for row in db_zyukugo:
#         zyukugo.append({'zyukugo': row[0]})
#     return render_template('index2.html',zyukugo=zyukugo)


@app.route('/index2')
def index2():
    zyukugo = zyukugos[0]
    return render_template('index2.html',zyukugo=zyukugo)


# @app.route('/index3')
# def index3():
#     con = sqlite3.connect(DATABASE)
#     db_zyukugo = con.execute('SELECT * FROM zyukugo LIMIT 1').fetchall()
#     db_characters = con.execute('SELECT * FROM characters').fetchall()
#     con.close()
#     zyukugo = []
#     characters = []
#     for row in db_zyukugo:
#         zyukugo.append({'zyukugo': row[0]})
#     for row in db_characters:
#         characters.append(row[0])
#     print(characters)
#     return render_template('index3.html',zyukugo=zyukugo, characters=characters)

@app.route('/index3')
def index3():
    zyukugo = zyukugos[0]
    print(characters)
    return render_template('index3.html',zyukugo=zyukugo, characters=characters)


# @app.route('/delete', methods=['POST'])
# def delete():
#     con = sqlite3.connect(DATABASE)
#     db_zyukugo_top = con.execute('SELECT * FROM zyukugo LIMIT 1').fetchall()
#     for i in range(len(db_zyukugo_top)):
#         db_zyukugo_top[i] = str(db_zyukugo_top[i])
#     print(type(db_zyukugo_top[0][2]))
#     print(db_zyukugo_top[0][2]) #一文字目が「(」、二文字目が「'」のため、三文字目[2]から数える

#     con.execute('delete from zyukugo where zyukugo = (select * from zyukugo limit 1 offset 0);') #１行目を削除
#     db_zyukugo_top = request.form['db_zyukugo_top']
#     con.execute('INSERT INTO zyukugo VALUES(?)',[db_zyukugo_top])
#     con.commit()
#     con.close()
#     return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete():
    a = zyukugos[0]
    zyukugos.pop(0)
    zyukugos.append(a)
    characters.clear()
    print(zyukugos[0])
    print(zyukugos[-1])
    return redirect(url_for('index'))



# @app.route('/register_character', methods=['POST'])
# def register_character():
#     copyimg = request.form['copyimg']
#     print(copyimg)

#     engines = pyocr.get_available_tools()
#     engine = engines[0]
#     dirname= 'idake.png' #この関数内でbsでスクレイピングした写真をとりいれ、読み込んだひらがなをDBに保存
#     txt = engine.image_to_string(Image.open(dirname), lang="jpn", builder=pyocr.builders.TextBuilder(tesseract_layout=10))

#     # for i in range(7):
#     #     dirname= '{}.png'.format(i)
#     #     txt = engine.image_to_string(Image.open(dirname), lang="jpn", builder=pyocr.builders.TextBuilder(tesseract_layout=10))
#     #     con = sqlite3.connect(DATABASE)
#     #     con.execute('INSERT INTO characters VALUES(?)',[txt])

#     con = sqlite3.connect(DATABASE)
#     con.execute('INSERT INTO characters VALUES(?)',[txt])
#     chara_list.append(txt)
#     con.commit()
#     con.close()
#     return redirect(url_for('index2'))





@app.route('/register_character', methods=['POST'])
def register_character():
    os.chmod("Tesseract-OCR/tesseract.exe",0o777)
    # root = "https://kyousei-tyan.herokuapp.com/"
    # url = "https://kyousei-tyan.herokuapp.com/index2"
    # # store_path = "C:\\Users\\ymnk1\\GeekSalon\\OCR2\\pafumepic.png" #\は二つ！！
    # store_path = "idake.png" #\は二つ！！
    # def img_store(path):
    #     img = requests.get(path).content

    #     print(path)

    #     with open(store_path, "wb") as f:
    #         f.write(img)

    #     img_local = cv2.cvtColor(cv2.imread(store_path), cv2.COLOR_BGR2RGB)

    #     plt.imshow(img_local)
    #     plt.show()
    # response = requests.get(url)
    # soup = BeautifulSoup(open('templates/index2.html', encoding="utf-8"), "html.parser") #書式を指定しないとUnicodeDecodeErrorになる
    # # soup = BeautifulSoup(url, "html.parser")
    # print(soup)
    # top_img2 = soup.find("div", id="bs").find("img", id="copyImg").get("src") #classを指定するときは「class_」で表すことに注意！！
    # print(top_img2)
    # img_url=root+top_img2 #img_urlは実際に写真自体をパスに指定しなければならない(フォルダじゃない！！)
    # img_store(img_url)
    


    engine = pyocr.libtesseract

    dirname= 'idake.png' #この関数内でbsでスクレイピングした写真をとりいれ、読み込んだひらがなをDBに保存
    txt = engine.image_to_string(Image.open(dirname), lang="jpn", builder=pyocr.builders.TextBuilder(tesseract_layout=10))

    characters.append(txt)
    print(characters)
    return redirect(url_for('index2'))


# @app.route('/register_character', methods=['POST','GET'])
# def register_character():
#     file = './base.jpg'
#     base_image = Image.open(file)
#     base_image = np.asarray(base_image)

#     for i in range(len(zyukugos[0])):





    # copyimg = request.form['copyimg']
    # print(copyimg)

    # engines = pyocr.get_available_tools()
    # engine = engines[0]
    # dirname= 'idake.png' #この関数内でbsでスクレイピングした写真をとりいれ、読み込んだひらがなをDBに保存
    # txt = engine.image_to_string(Image.open(dirname), lang="jpn", builder=pyocr.builders.TextBuilder(tesseract_layout=10))

    # characters.append(txt)
    # print(characters)
    # return redirect(url_for('index2'))

    

# @app.route('/insert', methods=['POST'])
# def insert():
#     zyukugo = request.form['zyukugo']

#     con = sqlite3.connect(DATABASE)
#     con.execute('INSERT INTO zyukugo VALUES(?)',[zyukugo])
#     con.commit()
#     con.close()
#     return redirect(url_for('index'))





# @app.route('/form')
# def form():
#     return render_template('form.html')

# @app.route('/register', methods=['POST'])
# def register():
#     zyukugo = request.form['zyukugo']

#     con = sqlite3.connect(DATABASE)
#     con.execute('INSERT INTO zyukugo VALUES(?)',[zyukugo])
#     con.commit()
#     con.close()
#     return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(port=22222)

#if __name__ == "__main__": をいれる