#!/usr/bin/python3
import sqlite3
from sqlite3 import Error

DBPATH = r"kvtmozi.sl3"

class KonyvtarMoziDB:
    '''Az adatbáziskezeléshez szükséges objektum'''
    def __init__(self,aDatabaseFile):
        try:
            self.database = sqlite3.connect(aDatabaseFile)
        except Error as errorMessage:
            self.error = errorMessage
    
    def getDatas(self, asql, adata):
        self.__getcur = self.database.cursor()
        self.__getcur.execute(asql,adata)
        self.datas = self.__getcur.fetchall()
        return self.datas

    def setDatas(self, asql, adata):
        self.__setcur = self.database.cursor()
        self.__setcur.execute(asql,adata)
        self.database.commit() 
