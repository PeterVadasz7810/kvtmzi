#!/usr/bin/python3

import kvtmoziweb
import json

with open ('mozipontok.json', encoding='utf-8') as json_data:
    mpoints = json.load(json_data)

foto_oldal = kvtmoziweb.WebLetszam("http://konyvtarmozi.hu/letszam.aspx")

print(foto_oldal.adatkuldes({'A':'b'}))
