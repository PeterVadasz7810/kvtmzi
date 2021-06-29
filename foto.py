#!/usr/bin/python3
from kvtmozivetites import correct_date

def get_photo(film,helyszin,datum,datalist):
    foto = 0
    for data in datalist:
        #print(data)
        if (data['Helyszin'].split()[0] == helyszin) and (data['Film'] == film) and (correct_date(data['Datum']) == datum):
            foto = 1
            break
    return foto
