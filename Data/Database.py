# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

from typing import List
from Data.Modeli import *

import Data.auth_public as auth
from datetime import date


class Repo:

    def __init__(self):
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=5432)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


    def Izdelki(self) -> List[IzdelekDto]: 
        izdelki = self.cur.execute(
            """
            SELECT i.id, i.ime, k.oznaka FROM Izdelki i
            left join KategorijaIzdelka k on i.kategorija = k.id
            """)

        return [IzdelekDto(id, ime, oznaka) for (id, ime, oznaka) in izdelki]
    
    def cena_izdelkov(self) -> List[CenaIzdelkaDto]:

        
        self.cur.execute(
            """
            select c.id, i.id as izdelek_id, i.ime, k.oznaka, c.leto, c.cena from cenaizdelka c
                left join izdelek i on i.id = c.izdelek_id
                left join kategorijaizdelka k on k.id = i.kategorija;
             """
        )

        return [CenaIzdelkaDto(id, izdelek_id, ime, oznaka, leto, cena) for (id, izdelek_id, ime, oznaka, leto, cena) in self.cur.fetchall()]
    
    def dobi_izdelek(self, ime_izdelka: str) -> Izdelek:
        # Preverimo, če izdelek že obstaja
        self.cur.execute("""
            SELECT id, ime, kategorija from Izdelek
            WHERE ime = %s
          """, (ime_izdelka,))
        
        row = self.cur.fetchone()

        if row:
            id, ime, kategorija = row
            return Izdelek(id, ime, kategorija)
        
        raise Exception("Izdelek z imenom " + ime_izdelka + " ne obstaja")

    
    def dodaj_izdelek(self, izdelek: Izdelek) -> Izdelek:

        # Preverimo, če izdelek že obstaja
        self.cur.execute("""
            SELECT id, ime, kategorija from Izdelek
            WHERE ime = %s
          """, (izdelek.ime,))
        
        row = self.cur.fetchone()
        if row:
            izdelek.id = row[0]
            return izdelek

        
    

        # Sedaj dodamo izdelek
        self.cur.execute("""
            INSERT INTO Izdelek (ime, kategorija)
              VALUES (%s, %s) RETURNING id; """, (izdelek.ime, izdelek.kategorija))
        izdelek.id = self.cur.fetchone()[0]
        self.conn.commit()
        return izdelek


    def dodaj_kategorijo(self, kategorija: KategorijaIzdelka) -> KategorijaIzdelka:


        # Preverimo, če določena kategorija že obstaja
        self.cur.execute("""
            SELECT id from KategorijaIzdelka
            WHERE oznaka = %s
          """, (kategorija.oznaka,))
        
        row = self.cur.fetchone()
        
        if row:
            kategorija.id = row[0]
            return kategorija


        # Če še ne obstaja jo vnesemo in vrnemo njen id
        self.cur.execute("""
            INSERT INTO KategorijaIzdelka (oznaka)
              VALUES (%s) RETURNING id; """, (kategorija.oznaka,))
        self.conn.commit()
        kategorija.id = self.cur.fetchone()[0]

        

        return kategorija
    
    def dodaj_ceno_izdelka(self, cena_izdelka: CenaIzdelka) -> CenaIzdelka:

         # Preverimo, če določena kategorija že obstaja
        self.cur.execute("""
            SELECT id, izdelek_id, leto, cena from CenaIzdelka
            WHERE izdelek_id = %s and leto = %s
          """, (cena_izdelka.izdelek_id, date(int(cena_izdelka.leto), 1, 1)))
        
        row = self.cur.fetchone()
        if row:
            cena_izdelka.id = row[0]
            return cena_izdelka
        
        # Dodamo novo ceno izdelka

        self.cur.execute("""
            INSERT INTO CenaIzdelka (izdelek_id, leto, cena)
              VALUES (%s, %s, %s) RETURNING id; """, (cena_izdelka.izdelek_id, date(int(cena_izdelka.leto), 1, 1), cena_izdelka.cena,))
        self.conn.commit()

        cena_izdelka.id = self.cur.fetchone()[0]
        return cena_izdelka

            

    







    

