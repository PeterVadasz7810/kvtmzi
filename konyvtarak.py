#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup as BS
import json
import sqlite3
from sqlite3 import Error

def getlibraries():

    ua = 'Mozilla/5.0 (Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
    header = {'User-Agent':ua}

    # Lekérjük a weboldalt
    page=requests.get('http://konyvtarmozi.hu/letszam.aspx', headers=header) 

    # Feldolgozzuk az oldal tartalmát
    pagedata=BS(page.content,'html.parser')

    # Megkeressük a feldolgozandó adatot
    tag=pagedata.find("select",attrs={"id":"ctl00_ContentPlaceHolder1_DropDownListKonyvtar"})

    with open ('telepulesek.json') as json_data:
        mpoints = json.load(json_data)

    libraries = []
    for tags in tag.find_all("option"):
        #Soronként kigyűtjük a könyvtárakat és a hozzájuk tartozó azonosítókat
        if tags.string.split()[0] in mpoints['telepulesek']:
            lib_data = dict(lib=tags.string.split()[0], id=tags.get("value"))
            libraries.append(lib_data)
    
    return libraries

def create_connection(database_file):
    database = None
    try:
        database = sqlite3.connect(database_file)
    except Error as e:
        print (e)
    return database

def add_lib(database, libdata):
    sql = '''INSERT INTO Library(SiteLibID,Village) VALUES(?,?)'''
    cur = database.cursor()
    cur.execute(sql, libdata)
    database.commit()
    return cur.lastrowid

def get_libID(database, libdata):
    sql ='''SELECT LibID FROM Library WHERE SiteLibID = ? AND Village = ?'''
    cur = database.cursor()
    cur.execute(sql,libdata)
    libID = cur.fetchall()
    return libID

def konyvtarlista_frissit():
    db = r"kvtmozi.sl3"
    lib_list = getlibraries()
    conn = create_connection(db)
    with conn:
        for lib in lib_list:
            lib_data = (lib['id'],lib['lib'])
            if len(get_libID(conn,lib_data)) == 0:
                add_lib(conn, lib_data)

if __name__ == "__main__":
   konyvtarlista_frissit()
