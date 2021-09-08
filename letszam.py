#!/usr/bin/python3
from kvtmozivetites import correct_date
import requests
from bs4 import BeautifulSoup as BS
import time
import random

'''
Lekérem az oldalt
Film:
    Kigyűjtöm az INPUT mezőket és tartalmukat
    Módosítom a szükséges INPUT/Select mezőket
    visszaküldöm az adatokat
Mozipont:
    Kigyűjtöm az INPUT mezőket és tartalmukat
    Módosítom a szükséges INPUT/Select mezőket
    visszaküldöm az adatokat
Vetítés
    Kigyűjtöm az INPUT mezőket és tartalmukat
    Módosítom a szükséges INPUT/Select mezőket
    visszaküldöm az adatokat

Kikeresem a létszámadatokat.

POST Request elemek:
__EVENTTARGET (ctl00$ContentPlaceHolder1$DropDownListFilm, ctl00$ContentPlaceHolder1$DropDownListKonyvtar, ctl00$ContentPlaceHolder1$GridViewVetitesek)
__EVENTARGUMENT (Kiválaszt gombra: Select$0..999)
__LASTFOCUS
__VIEWSTATE (Értékét lekérni, POSTtal küldeni)

__VIEWSTATEGENERATOR (Értékét lekérni, POSTtal küldeni)
__VIEWSTATEENCRYPTED
__EVENTVALIDATION (Értékét lekérni, POSTtal küldeni)
ctl00$ContentPlaceHolder1$DropDownListFilm
ctl00$ContentPlaceHolder1$DropDownListKonyvtar (Film után mindig 138!)

Kiválaszt gomb megkereséséhez: table, id:ctl00_ContentPlaceHolder1_GridViewVetitesek

input id-k Ezekből kell a value értéke:
ctl00_ContentPlaceHolder1_TextBoxGyerek
ctl00_ContentPlaceHolder1_TextBoxFelnott
ctl00_ContentPlaceHolder1_TextBoxNagyi
'''

def get_site (put_get, URL, params):
    '''
        Get the site with given useragent and parse that
        put_get: 0 if use get, 1 if use put. 
        URL: that you want to download, etc.
        params: dictionary which contains data, what you want to send the site. 
        return: the parsed site.
    '''
    ua = 'Mozilla/5.0 (Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
    header = {'User-Agent':ua}
    
    if put_get == 0:
        LetszamOldal = requests.get(URL, headers=header)
    elif put_get == 1:
        LetszamOldal = requests.post(URL,  data=params, headers=header)
    else:
        print ("Az első paraméter csak 0 vagy 1 lehet!!!")

    LetszamData = BS(LetszamOldal.content,'html.parser')
    return LetszamData

def get_all_input(LetszamData):
    #Get all inputs from site

    data = {}
    inputs = LetszamData.findAll('input')

    for inpt in inputs:
        data[inpt['name']]=inpt['value']
    return data

def get_all_select(LetszamData):
    data = {}
    selects = LetszamData.findAll('select')

    for select in selects:
        data[select['name']] = ''
    return data

def get_input_value(LetszamData,inputid):
    inp = LetszamData.find("input",attrs={"id":inputid})
    return inp.get('value')

def get_event_date_table(LetszamData,tableid):
    table = LetszamData.find("table",attrs={"id":tableid})
    Tfej = [th.get_text() for th in table.find("tr").find_all("th")]

    # A többi adat
    Adatok = []
    i = 0
    for Sor in table.find_all("tr")[1:]:
        Adat = dict(zip(Tfej, (td.get_text() for td in Sor.find_all("td"))))
        Adat['sid'] = Adat.pop('\xa0')+'Select$' + str(i)
        i+=1
        Adatok.append(Adat)
    return Adatok

def get_letszam(LibID, FilmID, EventDate):
    # constans values:
    const = {'URL':'http://konyvtarmozi.hu/letszam.aspx',\
        'EVENTTARGET':'__EVENTTARGET',\
        'EVENTARGUMENT':'__EVENTARGUMENT',\
        'LASTFOCUS':'__LASTFOCUS',\
        'VIEWSTATE':'__VIEWSTATE',\
        'VIEWSTATEGENERATOR':'__VIEWSTATEGENERATOR',\
        'VIEWSTATEENCRYPTED':'__VIEWSTATEENCRYPTED',\
        'EVENTVALIDATION':'__EVENTVALIDATION',\
        'DROPDOWNLISTFILM':'ctl00$ContentPlaceHolder1$DropDownListFilm',\
        'DROPDOWNLISTKONYVTAR':'ctl00$ContentPlaceHolder1$DropDownListKonyvtar'}
    
    # phase 1: dowload site
    LetszamOldal = get_site(0, const['URL'],'')
    input_dict = get_all_input(LetszamOldal)
    select_dict = get_all_select(LetszamOldal)
    data = {**input_dict,**select_dict}
    
    # phase 2: send selected Film and get the site again with some sleep
    data[const['DROPDOWNLISTFILM']] = FilmID
    data[const['DROPDOWNLISTKONYVTAR']] = '138'
    data[const['EVENTTARGET']] = 'ctl00$ContentPlaceHolder1$DropDownListFilm'
    time.sleep(random.randint(5,20))
    LetszamOldal = get_site(1,const['URL'],data)

    # phase 3: send selected Library and get the site again with some sleep
    data[const['DROPDOWNLISTFILM']] = FilmID
    data[const['DROPDOWNLISTKONYVTAR']] = LibID
    data[const['EVENTTARGET']] = 'ctl00$ContentPlaceHolder1$DropDownListKonyvtar'
    data[const['VIEWSTATE']] = get_input_value(LetszamOldal,const['VIEWSTATE'])
    data[const['VIEWSTATEGENERATOR']] = get_input_value(LetszamOldal,const['VIEWSTATEGENERATOR'])
    data[const['EVENTVALIDATION']] = get_input_value(LetszamOldal,const['EVENTVALIDATION'])
    time.sleep(random.randint(5,20))
    LetszamOldal = get_site(1,const['URL'],data)
    
    # phase 4: send selected Event and get the site again with some sleep 
    dictlist = get_event_date_table(LetszamOldal,'ctl00_ContentPlaceHolder1_GridViewVetitesek')
    for dict in dictlist:
        if correct_date(dict['Dátum']) == EventDate:
            if data[const['EVENTARGUMENT']] == '':
                data[const['EVENTARGUMENT']] = dict['sid']
            else:
                print(f'Időpontütközés!!! - {data[const["EVENTARGUMENT"]]}')
                data[const['EVENTARGUMENT']] = dict['sid']

    data[const['DROPDOWNLISTFILM']] = FilmID
    data[const['DROPDOWNLISTKONYVTAR']] = LibID
    data[const['EVENTTARGET']] = 'ctl00$ContentPlaceHolder1$GridViewVetitesek'
    data[const['VIEWSTATE']] = get_input_value(LetszamOldal,const['VIEWSTATE'])
    data[const['VIEWSTATEGENERATOR']] = get_input_value(LetszamOldal,const['VIEWSTATEGENERATOR'])
    data[const['EVENTVALIDATION']] = get_input_value(LetszamOldal,const['EVENTVALIDATION'])
    time.sleep(random.randint(5,20))
    LetszamOldal = get_site(1,const['URL'],data)
    #return {'Gyerek':get_input_value(LetszamOldal,'ctl00_ContentPlaceHolder1_TextBoxGyerek'),'Felnőtt':get_input_value(LetszamOldal,'ctl00_ContentPlaceHolder1_TextBoxFelnott'),'Nagyi':get_input_value(LetszamOldal,'ctl00_ContentPlaceHolder1_TextBoxNagyi')}
    return [get_input_value(LetszamOldal,'ctl00_ContentPlaceHolder1_TextBoxGyerek'),get_input_value(LetszamOldal,'ctl00_ContentPlaceHolder1_TextBoxFelnott'),get_input_value(LetszamOldal,'ctl00_ContentPlaceHolder1_TextBoxNagyi')]

if __name__ == "__main__":
   print(get_letszam("271","37","2020-11-04 16:00:00"))
