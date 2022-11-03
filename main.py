# from flaskr import app
from flask import Flask, render_template, request, redirect, url_for
import db
from PIL import Image
import pyocr
import base64
import requests
from bs4 import BeautifulSoup

pyocr.tesseract.TESSERACT_CMD = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' #これ入れないと動かないっぽい(デバッグ10/13)
db.create_zyukugo_table()
db.create_characters_table()
import sqlite3
DATABASE = 'database.db'

# app = Flask(__name__)
app = Flask(__name__, static_folder='static')

# @app.route('/')
# def index():
#     con = sqlite3.connect(DATABASE)
#     db_zyukugo = con.execute('SELECT * FROM zyukugo').fetchall()
#     con.close()

#     zyukugo = []
#     for row in db_zyukugo:
#         zyukugo.append({'title': row[0], 'price': row[1], 'arrival_day': row[2]})


@app.route('/')
def index():
    # con = sqlite3.connect(DATABASE)
    # db_zyukugo = con.execute('SELECT * FROM zyukugo').fetchall()
    # con.close()
    # zyukugo = []
    # for row in db_zyukugo:
    #     zyukugo.append({'zyukugo': row[0]})
    return render_template('index.html')

@app.route('/index2')
def index2():
    con = sqlite3.connect(DATABASE)
    db_zyukugo = con.execute('SELECT * FROM zyukugo LIMIT 1').fetchall()
    con.close()
    zyukugo = []
    for row in db_zyukugo:
        zyukugo.append({'zyukugo': row[0]})
    return render_template('index2.html',zyukugo=zyukugo)


@app.route('/index3')
def index3():
    con = sqlite3.connect(DATABASE)
    db_zyukugo = con.execute('SELECT * FROM zyukugo LIMIT 1').fetchall()
    db_characters = con.execute('SELECT * FROM characters').fetchall()
    con.close()
    zyukugo = []
    characters = []
    for row in db_zyukugo:
        zyukugo.append({'zyukugo': row[0]})
    for row in db_characters:
        characters.append(row[0])
    print(characters)
    return render_template('index3.html',zyukugo=zyukugo, characters=characters)


@app.route('/delete', methods=['POST'])
def delete():
    # zyukugo = request.form['zyukugo']
    # db_zyukugo = con.execute('DELETE * FROM zyukugo LIMIT 1').fetchall()

    con = sqlite3.connect(DATABASE)
    # db_zyukugo = con.execute('SELECT * FROM zyukugo').fetchall()
    db_zyukugo_top = con.execute('SELECT * FROM zyukugo LIMIT 1').fetchall()
    # db_zyukugo_top = str()
    for i in range(len(db_zyukugo_top)):
        db_zyukugo_top[i] = str(db_zyukugo_top[i])
    print(type(db_zyukugo_top[0][2]))
    print(db_zyukugo_top[0][2]) #一文字目が「(」、二文字目が「'」のため、三文字目[2]から数える


    # con.execute('INSERT INTO zyukugo VALUES(?)',[db_zyukugo_top])
    # db_zyukugo.append(db_zyukugo_top)
    con.execute('delete from zyukugo where zyukugo = (select * from zyukugo limit 1 offset 0);') #１行目を削除
    db_zyukugo_top = request.form['db_zyukugo_top']
    con.execute('INSERT INTO zyukugo VALUES(?)',[db_zyukugo_top])
    con.commit()
    con.close()
    return redirect(url_for('index'))




@app.route('/register_character', methods=['POST'])
def register_character():
    copyimg = request.form['copyimg']
    print(copyimg)

    engines = pyocr.get_available_tools()
    engine = engines[0]
    dirname= 'idake.png' #この関数内でbsでスクレイピングした写真をとりいれ、読み込んだひらがなをDBに保存

    # dirname = 'aaa.png'
    txt = engine.image_to_string(Image.open(dirname), lang="jpn", builder=pyocr.builders.TextBuilder(tesseract_layout=10))

    # for i in range(7):
    #     dirname= '{}.png'.format(i)
    #     txt = engine.image_to_string(Image.open(dirname), lang="jpn", builder=pyocr.builders.TextBuilder(tesseract_layout=10))
    #     con = sqlite3.connect(DATABASE)
    #     con.execute('INSERT INTO characters VALUES(?)',[txt])

    con = sqlite3.connect(DATABASE)
    con.execute('INSERT INTO characters VALUES(?)',[txt])
    con.commit()
    con.close()
    return redirect(url_for('index2'))

    

@app.route('/insert', methods=['POST'])
def insert():
    zyukugo = request.form['zyukugo']

    con = sqlite3.connect(DATABASE)
    con.execute('INSERT INTO zyukugo VALUES(?)',[zyukugo])
    con.commit()
    con.close()
    return redirect(url_for('index'))



@app.route('/form')
def form():
    return render_template('form.html')

# @app.route('/register', methods=['POST'])
# def register():
#     title = request.form['title']
#     price = request.form['price']
#     arrival_day = request.form['arrival_day']

#     con = sqlite3.connect(DATABASE)
#     con.execute('INSERT INTO zyukugo VALUES(?, ?, ?)',[title, price, arrival_day])
#     con.commit()
#     con.close()
#     return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    zyukugo = request.form['zyukugo']

    con = sqlite3.connect(DATABASE)
    con.execute('INSERT INTO zyukugo VALUES(?)',[zyukugo])
    con.commit()
    con.close()
    return redirect(url_for('index'))


app.run(port=8000, debug=True)