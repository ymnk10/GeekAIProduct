import sqlite3

DATABASE = 'database.db'

def create_zyukugo_table(): 
    con= sqlite3.connect(DATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS zyukugos (zyukugo)")
    con.close() #zyukugoに変更

def create_characters_table():
    con= sqlite3.connect(DATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS characters (character)")
    con.close() #characters