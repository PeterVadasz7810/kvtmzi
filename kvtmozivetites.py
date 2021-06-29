#!/usr/bin/python3

def correct_date(indate):
    ind = indate.replace('. ',' ').replace('.','-')
    tmpdate = ind.split()
    if len(tmpdate[1]) != 8:
        tmpdate[1] = f'0{tmpdate[1]}' 
    return f'{tmpdate[0]} {tmpdate[1]}'

class KonyvtarMoziVetites:
    '''
        A vetítés adatait tartalmazó objektum.
    '''
    def __init__(self, aKonyvtar, aFilm, aDatum, aVendeg, aProgram):
        '''Init metódus:
            Paraméterek:
            aKonyvtar: String, a Település neve, ahol a könyvtármozi pont van
            aFilm: String, a Film címe, amit vetített
            aDatum: String, a vetítés dátuma
            aVendeg: String, a vetítés vendége
            aProgram: String, a vetítéshez kapcsolódó program
        '''
        self.konyvtar = aKonyvtar
        self.film = aFilm
        self.datum = correct_date(aDatum)
        self.vendeg = aVendeg
        self.program = aProgram

    def __str__(self):
        tmpSTR = f'Település: {self.konyvtar}\tFilm: {self.film}\tDátum: {self.datum}\tVendég: {self.vendeg}\tProgram: {self.program}'
        return tmpSTR
    
    def setGyerekLetszam(self, aGyerekdb):
        self.gyerekletszam = int(aGyerekdb)
    
    def setFelnottLetszam(self,aFelnottdb):
        self.felnottletszam = int(aFelnottdb)
    
    def setNagyiLetszam(self,aNagyidb):
        self.nagyiletszam = int(aNagyidb)

    def setVanFoto(self, aVanFoto):
        self.vanfoto = aVanFoto

    def setVetitesID(self, aVetitesID):
        self.vetitesID = aVetitesID
    
    def setFilmID(self, aFilmID):
        self.filmID = aFilmID
    
    def setKonyvtarID(self, aKonyvtarID):
        self.konyvtarID = aKonyvtarID

    def getEventData(self):
        #TODO ellenőrzést megírni konyvtarID-re és filmID-re!
        self.event_data = (self.konyvtarID, self.filmID, self.datum, self.program, self.vendeg)
        return self.event_data
