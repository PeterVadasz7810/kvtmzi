CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE Librarian (LibrarianID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, Name TEXT NOT NULL, "E-mail" TEXT NOT NULL, Phone TEXT NOT NULL);
CREATE TABLE Event (EventID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, LibID INTEGER REFERENCES Library (LibID) ON DELETE SET NULL ON UPDATE CASCADE NOT NULL, FilmID INTEGER REFERENCES Film (FilmID) ON DELETE SET NULL ON UPDATE CASCADE NOT NULL, Date REAL, Program TEXT, Guest TEXT, Child INTEGER NOT NULL DEFAULT (0), Adult INTEGER NOT NULL DEFAULT (0), Granny INTEGER NOT NULL DEFAULT (0), Photo INTEGER DEFAULT (0));
CREATE TABLE Library (LibID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, SiteLibID INTEGER UNIQUE NOT NULL, Village STRING UNIQUE NOT NULL, Deleted BOOLEAN, DelDate DATE);
CREATE INDEX idxName ON Librarian (Name COLLATE NOCASE ASC);
CREATE INDEX idxDate ON Event (Date COLLATE NOCASE ASC);
CREATE INDEX idxVillage ON Library (Village COLLATE NOCASE COLLATE NOCASE ASC);
CREATE VIEW "2020-as összesítő" AS SELECT
    Library.Village,
    SUM(Event.Child) AS Gyerek,
    SUM(Event.Adult) AS Felnőtt,
    SUM(Event.Granny) AS Nagyi
FROM
    Event
INNER JOIN Library ON Library.LibID = Event.LibID
WHERE
    date(Date) BETWEEN '2020-01-01' AND '2020-12-31'
GROUP BY
    Village
ORDER BY
    Village ASC
/* "2020-as összesítő"(Village,Gyerek,"Felnőtt",Nagyi) */;
CREATE VIEW "Fotó hiány" AS SELECT
    Library.Village AS Település,
    Film.Title AS Filmcím,
    Film.SiteFilmID,
    Library.SiteLibID,
    DateTime(Event.Date) AS Dátum
FROM
    Event
    INNER JOIN Film ON Film.FilmID = Event.FilmID
    INNER JOIN Library ON Library.LibID = Event.LibID
WHERE
    Event.Photo = 0
/* "Fotó hiány"("Település","Filmcím",SiteFilmID,SiteLibID,"Dátum") */;
CREATE VIEW "Legtöbbet vetített film" AS SELECT
    Film.Title,
    COUNT(*) AS "Vetítések száma",
    SUM(Child)+SUM(Adult)+SUM(Granny) AS "Látta (fő)"
FROM
    Event
    INNER JOIN Film ON Film.FilmID = Event.FilmID
GROUP BY 
    Event.FilmID
HAVING 
    COUNT(*) > 0
ORDER BY
    COUNT(*) DESC
LIMIT 20
/* "Legtöbbet vetített film"(Title,"Vetítések száma","Látta (fő)") */;
CREATE TABLE Film (FilmID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, SiteFilmID INTEGER UNIQUE NOT NULL, Title TEXT NOT NULL, Subtitle TEXT, Director TEXT, Creators TEXT, Actors TEXT, Year INTEGER, Length STRING, Description TEXT);
CREATE INDEX idxTitle ON Film (Title COLLATE NOCASE COLLATE NOCASE ASC);
CREATE VIEW "Vetítések (összes)" AS SELECT 
    Library.Village AS Település,
    Film.Title AS Filmcím,
    date(Date) AS Dátum,
    time(Date) AS Időpont,
    Guest AS Vendég,
    Program,
    Child AS Gyerek,
    Adult AS Felnőtt,
    Granny AS Nagyi,
    (Child+Adult+Granny) AS Összesen
FROM
    Event
    INNER JOIN Library ON Library.LibID = Event.LibID
    INNER JOIN Film ON Film.FilmID = Event.FilmID
ORDER BY
    Dátum DESC,
    Időpont DESC
/* "Vetítések (összes)"("Település","Filmcím","Dátum","Időpont","Vendég",Program,Gyerek,"Felnőtt",Nagyi,"Összesen") */;
CREATE VIEW "Vetítések 2021" AS SELECT 
    Library.Village AS Település,
    Film.Title AS Filmcím,
    date(Date) AS Dátum,
    time(Date) AS Időpont,
    Guest AS Vendég,
    Program,
    Child AS Gyerek,
    Adult AS Felnőtt,
    Granny AS Nagyi,
    (Child+Adult+Granny) AS Összesen
FROM
    Event
    INNER JOIN Library ON Library.LibID = Event.LibID
    INNER JOIN Film ON Film.FilmID = Event.FilmID
WHERE
    Dátum BETWEEN '2020-12-31' AND '2022-01-01'
ORDER BY
    Dátum DESC,
    Időpont DESC
/* "Vetítések 2021"("Település","Filmcím","Dátum","Időpont","Vendég",Program,Gyerek,"Felnőtt",Nagyi,"Összesen") */;
CREATE VIEW "Létszám összesítő" AS SELECT 
    SUM(Child) AS Gyerek,
    SUM(Adult) AS Felnőtt,
    SUM(Granny) AS Nagyi,
    (SUM(Child)+SUM(Adult)+SUM(Granny)) AS Összesen,
    COUNT(EventID) AS "Vetítések száma"
FROM Event
/* "Létszám összesítő"(Gyerek,"Felnőtt",Nagyi,"Összesen","Vetítések száma") */;
CREATE VIEW "Létszám hiány" AS SELECT
    Library.Village AS Település,
    Film.Title AS Filmcím,
    Film.SiteFilmID,
    Library.SiteLibID,
    DateTime(Event.Date) AS Dátum
FROM
    Event
    INNER JOIN Film ON Film.FilmID = Event.FilmID
    INNER JOIN Library ON Library.LibID = Event.LibID
WHERE
    Child+Adult+Granny = 0
/* "Létszám hiány"("Település","Filmcím",SiteFilmID,SiteLibID,"Dátum") */;
CREATE VIEW "Vetítések 2020" AS SELECT 
    Library.Village AS Település,
    Film.Title AS Filmcím,
    date(Date) AS Dátum,
    time(Date) AS Időpont,
    Guest AS Vendég,
    Program,
    Child AS Gyerek,
    Adult AS Felnőtt,
    Granny AS Nagyi,
    (Child+Adult+Granny) AS Összesen
FROM
    Event
    INNER JOIN Library ON Library.LibID = Event.LibID
    INNER JOIN Film ON Film.FilmID = Event.FilmID
WHERE
    Dátum BETWEEN '2019-12-31' AND '2021-01-01'
ORDER BY
    Dátum DESC,
    Időpont DESC
/* "Vetítések 2020"("Település","Filmcím","Dátum","Időpont","Vendég",Program,Gyerek,"Felnőtt",Nagyi,"Összesen") */;
CREATE VIEW "Utoljára vetített" AS SELECT
    DateTime(MAX(Event.Date)) AS "Utolsó vetítés",
    Library.Village
FROM
    Library
    INNER JOIN Event ON Event.LibID = Library.LibID
WHERE
    Library.Deleted <> 1
GROUP BY Event.LibID
ORDER BY "Utolsó vetítés" DESC
/* "Utoljára vetített"("Utolsó vetítés",Village) */;
