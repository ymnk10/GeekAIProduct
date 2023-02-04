#!/usr/bin/python

#コメントアウト色々含んだバージョンはgooglekeep「kyou-sei-tyan app.pyコード(2/4)」に記載
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import pyocr
import base64
import numpy as np
from io import BytesIO
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import cv2 #pipでもインストールしたら解決
import os
import re

pyocr.tesseract.TESSERACT_CMD = '/app/.apt/usr/bin/tesseract' #パブリッシュした時はこっちで動かす
# pyocr.tesseract.TESSERACT_CMD = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" #ローカルの時はこっちで動かす


app = Flask(__name__, static_folder='static')

characters = []
characters_eng = []
engines = pyocr.get_available_tools()
engine = engines[0]

tangos = ['WORLD','BECAUSE','THOSE','COULD','first','even','through','after','never','most','another','while','begin','problem','during','number','believe','WOULD']

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



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/index2')
def index2():
    zyukugo = zyukugos[0]
    return render_template('index2.html',zyukugo=zyukugo, characters=characters)

@app.route('/index4')
def index4():
    tango = tangos[0]
    return render_template('index4.html',tango=tango, characters_eng=characters_eng)

@app.route('/index3')
def index3():
    zyukugo = zyukugos[0]
    print(characters)
    return render_template('index3.html',zyukugo=zyukugo, characters=characters)

@app.route('/index5')
def index5():
    tango = tangos[0]
    print(characters_eng)
    return render_template('index5.html',tango=tango, characters_eng=characters_eng)


@app.route('/delete', methods=['POST'])
def delete():
    a = zyukugos[0]
    zyukugos.pop(0)
    zyukugos.append(a)
    characters.clear()
    characters_eng.clear()
    print(zyukugos[0])
    print(zyukugos[-1])
    return redirect(url_for('index'))

@app.route('/delete2', methods=['POST'])
def delete2():
    b = tangos[0]
    tangos.pop(0)
    tangos.append(b)
    characters.clear()
    characters_eng.clear()
    print(tangos[0])
    print(tangos[-1])
    return redirect(url_for('index'))


@app.route('/register_character', methods=['POST'])
def register_character():

    # ajax通信で送られた各画像データをデコードし骨格検出
    enc_data  = request.form["img1"]
    dec_data = base64.b64decode(enc_data.split(',')[1] ) # 環境依存の様(","で区切って本体をdecode)
    # print(dec_data)
    dec_img  = Image.open(BytesIO(dec_data)).convert('L')
    dec_img  = np.asarray(dec_img)
    dec_img = Image.fromarray(dec_img)
    # engines = pyocr.get_available_tools()
    # engine = engines[0]
    # print(engine)
    #  #この関数内でbsでスクレイピングした写真をとりいれ、読み込んだひらがなをDBに保存
    txt = engine.image_to_string(dec_img, lang="jpn", builder=pyocr.builders.TextBuilder(tesseract_layout=10))
    txt = txt.replace('W','ん')
    txt = txt.replace('w','ん')
    txt = txt.replace('N/','ん')
    txt = txt.replace('(こ','に')
    txt = txt.replace('(に','に')
    txt = txt.replace('ハ','い')
    txt = txt.replace('フ','う')
    txt = txt.replace('0','の')
    txt = txt.replace('の）','の')
    txt = txt.replace('マ','の')
    txt = txt.replace('[3','け')
    txt = txt.replace('い¥','い')
    txt = txt.replace('し¥','い')
    txt = txt.replace('し1','い')
    txt = txt.replace('い,','い')
    txt = txt.replace('は\'','は')

    characters.append(txt)
    print(characters)
    return redirect(url_for('index2'))


@app.route('/register_character_eng', methods=['POST'])
def register_character_eng():

    # ajax通信で送られた各画像データをデコードし骨格検出
    enc_data_eng  = request.form["img2"] #変更
    dec_data_eng = base64.b64decode(enc_data_eng.split(',')[1] ) # 環境依存の様(","で区切って本体をdecode)
    # print(dec_data)
    dec_img_eng  = Image.open(BytesIO(dec_data_eng)).convert('L')
    dec_img_eng  = np.asarray(dec_img_eng)
    dec_img_eng = Image.fromarray(dec_img_eng)


    # engines = pyocr.get_available_tools()
    # engine = engines[0]
    # print(engine)
    #  #この関数内でbsでスクレイピングした写真をとりいれ、読み込んだひらがなをDBに保存
    txt_eng = engine.image_to_string(dec_img_eng, lang="eng", builder=pyocr.builders.TextBuilder(tesseract_layout=10))
    txt_eng = txt_eng.replace('¥W','W')
    txt_eng = txt_eng.replace('W/','W')
    txt_eng = txt_eng.replace('@','O')
    txt_eng = txt_eng.replace('©','O')
    txt_eng = txt_eng.replace('0','O')
    txt_eng = txt_eng.replace('¥V','W')
    txt_eng = txt_eng.replace('VW','W')

    characters_eng.append(txt_eng)
    print(characters_eng)
    return redirect(url_for('index4'))

# if __name__ == "__main__":
#     app.run(port=22222, debug=True)

#if __name__ == "__main__": をいれる