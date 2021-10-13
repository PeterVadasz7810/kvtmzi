#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup as BS
import sqlite3
from sqlite3 import Error


def get_movie_details(filmID):
    table_header = ['Data', 'Content']

    ua = 'Mozilla/5.0 (Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
    header = {'User-Agent': ua}

    URL = f'http://konyvtarmozi.hu/filmReszletes.aspx?filmid={filmID}'

    # Lekérjük a weboldalt
    movie_details_page = requests.get(URL, headers=header)

    # Feldolgozzuk az oldal tartalmát
    movie_details_page_content = BS(movie_details_page.content, 'html.parser')

    # Megkeressük a feldolgozandó táblát
    movie_details = movie_details_page_content.find("table", attrs={"id": "ctl00_ContentPlaceHolder1_DetailsViewFilm"})

    # A többi adat
    Adatok = []

    for Sor in movie_details.find_all("tr"):
        Adat = dict(zip(table_header, (td.get_text() for td in Sor.find_all("td"))))
        Adatok.append(Adat)

    # Egy darab Dictionarybe tesszük az adatokat a listából
    data_dictionary = {}
    for datas in Adatok:
        if datas['Data'] == 'Hossz':
            data_dictionary[datas['Data']] = datas['Content'].replace('\xa0', 'Nincs').replace("'", " perc").replace(
                '"', ' másodperc')
        else:
            data_dictionary[datas['Data']] = datas['Content'].replace('\xa0', 'Nincs')

    return data_dictionary


def getmovies():
    ua = 'Mozilla/5.0 (Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
    header = {'User-Agent': ua}

    # Lekérjük a weboldalt
    page = requests.get('http://konyvtarmozi.hu/letszam.aspx', headers=header)

    # Feldolgozzuk az oldal tartalmát
    pagedata = BS(page.content, 'html.parser')

    # Megkeressük a feldolgozandó adatot
    tag = pagedata.find("select", attrs={"id": "ctl00_ContentPlaceHolder1_DropDownListFilm"})

    movies = []
    for tags in tag.find_all("option"):
        # Soronként kigyűtjük a filmcímeket és a hozzájuk tartozó azonosítókat
        moviedata = get_movie_details(
            tags.get("value"))  # eredetileg ez volt itt: dict(film=tags.string, id=tags.get("value"))
        moviedata['id'] = tags.get("value")
        movies.append(moviedata)

    return movies


def create_connection(database_file):
    database = None
    try:
        database = sqlite3.connect(database_file)
    except Error as e:
        print(e)
    return database


def add_movie(database, filmdata):
    sql = '''INSERT INTO Film(Title,Subtitle,Director,Creators,Actors,Year,Length,Description,SiteFilmID) VALUES(?,?,?,?,?,?,?,?,?)'''
    cur = database.cursor()
    cur.execute(sql, filmdata)
    database.commit()
    return cur.lastrowid


def update_films(database, filmdata):
    sql = '''UPDATE Film 
             SET Title = ?,
                 Subtitle = ?,
                 Director = ?,
                 Creators = ?,
                 Actors = ?,
                 Year = ?,
                 Length = ?,
                 Description = ?
            WHERE SiteFilmID = ?;       
          '''
    cur = database.cursor()
    cur.execute(sql, filmdata)
    database.commit()
    return cur.lastrowid


def get_movieID(database, filmdata):
    sql = '''SELECT FilmID FROM Film WHERE SiteFilmID = ?'''
    cur = database.cursor()
    cur.execute(sql, filmdata)
    movieID = cur.fetchall()
    return movieID


def get_field_null_value(database, filmdata):
    sql = '''SELECT FilmID FROM Film WHERE SiteFilmID = ? AND Subtitle IS NULL'''
    cur = database.cursor()
    cur.execute(sql, filmdata)
    movie_data = cur.fetchall()
    return movie_data


def title_changed(database, filmdata):
    sql = '''SELECT FilmID FROM Film WHERE SiteFilmID = ? AND title != ?'''
    cur = database.cursor()
    cur.execute(sql, filmdata)
    movie_data = cur.fetchall()
    return movie_data


def filmlista_frissit():
    db = r"kvtmozi.sl3"
    movie_list = getmovies()
    conn = create_connection(db)
    with conn:
        for film in movie_list:
            film_data = (
            film['Cím'], film['Alcím'], film['Rendező'], film['Alkotók'], film['Szereplők'], film['Év'], film['Hossz'],
            film['Leírás'], film['id'])
            if len(get_movieID(conn, [film['id']])) == 0:
                add_movie(conn, film_data)
            elif (len(get_field_null_value(conn, [film['id']])) != 0) or (
                    len(title_changed(conn, [film['id'], film['Cím']])) != 0):
                update_films(conn, film_data)


if __name__ == "__main__":
    filmlista_frissit()
