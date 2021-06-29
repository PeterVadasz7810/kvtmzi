#!/usr/bin/python3

import kvtmozivetites as KM
from kvtmozivetites import correct_date
import kvtmozidb as KMDB
import kvtmoziweb as KMWeb
from letszam import get_letszam
from foto import get_photo
from filmek import filmlista_frissit

def get_first_item(items):
    if len(items)!=0:
        return items[0][0]

def add_foto(db, event, sitedata):
    foto = get_first_item(db.getDatas('SELECT Photo FROM Event WHERE EventID=?',[event.vetitesID]))
    if foto == 0:
        db.setDatas('UPDATE Event SET Photo=? WHERE EventID=?',[get_photo(event.film,event.konyvtar,event.datum,sitedata),event.vetitesID])

def update_letszam(db, event_list):
    sql = '''
    UPDATE Event
    SET Child = ?,
        Adult = ?,
        Granny = ?
    WHERE EventID = ?
    '''
    for event in event_list:
        data_list = get_letszam(event[0],event[1],event[2])
        data_list.append(event[3])
        db.setDatas(sql,data_list)

def vetitesek():
    print('Filmlista frissítése...')
    filmlista_frissit()

    sql = '''
    SELECT Library.SiteLibID, Film.SiteFilmID, DateTime(Event.Date), Event.EventID 
    FROM Event 
    INNER JOIN Film ON Film.FilmID = Event.FilmID 
    INNER JOIN Library ON Library.LibID = Event.LibID 
    WHERE Child+Adult+Granny = 0
    '''
    print('Fotó oldal lekérése...')
    foto_oldal = KMWeb.WebFoto(KMWeb.URL_FOTOK)
    foto_oldal_adat_lista = [adat for adat in foto_oldal.foto_lista()]
    print('Vetítések oldal lekérése...')
    vetitesek = KMWeb.WebVetites(KMWeb.URL_VETITESEK)
 
    vetites_lista_all = [adat for adat in vetitesek.vetites_lista()]

    database = KMDB.KonyvtarMoziDB(KMDB.DBPATH)

    tmp_village_list = database.getDatas('SELECT Village FROM Library','')

    #village_list=[]
    #for village in tmp_village_list:
    #    village_list.append(village[0])
    
    village_list = [village[0] for village in tmp_village_list]

    del tmp_village_list
    vetites_lista = []

    print('Vetítések adatainak frissítése, új vetítések rögzítése...')
    for vetites in vetites_lista_all:

        if vetites['Intezmeny'].split()[0] in village_list:
            intezmeny = vetites['Intezmeny'].split()[0]
            village_id = get_first_item(database.getDatas('SELECT LibID FROM Library WHERE Village=?', [intezmeny]))
            film = vetites['Film']
            movie_id = get_first_item(database.getDatas('SELECT FilmID FROM Film WHERE Title=?',[film]))
            event_date = correct_date(vetites['Datum'])
            ev_data = (village_id,movie_id,event_date)
            event_id = get_first_item(database.getDatas('SELECT EventID FROM Event INNER JOIN Library ON Library.LibID = Event.LibID INNER JOIN Film ON Film.FilmID = Event.FilmID WHERE Library.LibID = ? AND Film.FilmID = ? AND Event.Date = julianday(?)',ev_data))
            event_prg = vetites['Kapcsolodo program'].replace('\xa0','Nincs')
            event_guest = vetites['Felvezeto vendeg'].replace('\xa0','Nincs')
            vetites_lista.append(KM.KonyvtarMoziVetites(intezmeny,film,event_date,event_guest,event_prg))
            vetites_lista[len(vetites_lista)-1].setFilmID(movie_id)
            vetites_lista[len(vetites_lista)-1].setKonyvtarID(village_id)
            vetites_lista[len(vetites_lista)-1].setVetitesID(event_id)
            if event_id != None:
                # print(f'Fotó oldal adatLista ELEJE: {foto_oldal_adat_lista} :Fotó oldal adatLista VÉGE')
                add_foto(database,vetites_lista[len(vetites_lista)-1],foto_oldal_adat_lista)
            if event_id == None:    
                database.setDatas('INSERT INTO Event(LibID,FilmID,Date,Program,Guest) VALUES(?,?,julianday(?),?,?)',vetites_lista[len(vetites_lista)-1].getEventData())
    print(f'Vetítések száma: {len(vetites_lista)}')
    print('Létszámadatok frissítése...')
    adatpotlas_lista = database.getDatas(sql,'')
    update_letszam(database, adatpotlas_lista)
    print('A műveletek sikeresen végrehajtásra kerültek.')
    
if __name__ == "__main__":
   vetitesek()