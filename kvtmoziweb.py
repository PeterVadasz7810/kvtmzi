#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup as BS
from unidecode import unidecode

URL_VETITESEK = "http://konyvtarmozi.hu/vetitesek.aspx"
URL_LETSZAM = "http://konyvtarmozi.hu/letszam.aspx"
URL_FOTOK = "http://konyvtarmozi.hu/kepesProgram.aspx"


class WebAdat:
    _USER_AGENT = 'Mozilla/5.0 (Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
    _header = {'User-Agent': _USER_AGENT}

    def __init__(self, siteURL):
        self.URL = siteURL
        self.refresh()

    def refresh(self):
        site = requests.get(self.URL, headers=self._header)
        self.web_content = BS(site.content, 'html.parser')


class WebFoto(WebAdat):
    __data_list = []

    def foto_lista(self, tableID='ctl00_ContentPlaceHolder1_GridViewVetitesek'):
        self.refresh()
        self.__data_list.clear()
        foto_tabla = self.web_content.find("table", attrs={"id": tableID})
        tabla_fej = [unidecode(th.get_text()) for th in foto_tabla.find("tr").find_all("th")]
        for row in foto_tabla.find_all("tr")[1:]:
            data = dict(zip(tabla_fej, (td.get_text() for td in row.find_all("td"))))
            self.__data_list.append(data)
        return self.__data_list


class WebVetites(WebFoto):

    def vetites_lista(self, tableID='ctl00_ContentPlaceHolder1_GridViewElmult'):
        return self.foto_lista(tableID)


class WebLetszam(WebAdat):
    _mozipont_lista = []
    _film_lista = []

    def get_film_lista(self, sID='ctl00_ContentPlaceHolder1_DropDownListFilm'):
        self._film_lista.clear()
        film_adatok = self.web_content.find("select", attrs={"id": sID})
        for film in film_adatok.find_all("option"):
            film_adat = dict(film=film.string, id=film.get("value"))
            self._film_lista.append(film_adat)
        return self._film_lista

    def get_konyvtar_lista(self, konyvtarak: list, sID='ctl00_ContentPlaceHolder1_DropDownListKonyvtar'):
        self._mozipont_lista.clear()
        konyvtarak_web = self.web_content.find("select", attrs={"id": sID})
        for konyvtar in konyvtarak_web.find_all("option"):
            if konyvtar.string.split()[0] in konyvtarak:
                konyvtar_adat = dict(lib=konyvtar.string.split()[0], id=konyvtar.get("value"))
                self._mozipont_lista.append(konyvtar_adat)
        return self._mozipont_lista

    def adatkuldes(self, kuldott_adat: dict):
        site = requests.post(self.URL, data=kuldott_adat, headers=self._header)
        self.web_content = BS(site.content, 'html.parser')
        return self.web_content
