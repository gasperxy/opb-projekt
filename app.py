#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottleext import get, post, run, request, template, redirect, static_file, url

# uvozimo ustrezne podatke za povezavo

from Data.Database import Repo
from Data.Modeli import *


import os

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# odkomentiraj, če želiš sporočila o napakah
# debug(True)

repo = Repo()

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')

@get('/')
def index():
    izdelki = repo.cena_izdelkov()
    return template('izdelki.html', izdelki=izdelki)

@get('/dodaj_izdelek')
def dodaj_izdelek():
    
    return template('dodaj_izdelek.html', izdelek = CenaIzdelkaDto())


######################################################################
# Glavni program



# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)
