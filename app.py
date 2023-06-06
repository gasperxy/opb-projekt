#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user


# uvozimo ustrezne podatke za povezavo

from Data.Database import Repo
from Data.Modeli import *
from Data.Services import AuthService
from functools import wraps

import os

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)


# odkomentiraj, če želiš sporočila o napakah
# debug(True)

repo = Repo()
auth = AuthService(repo)

def cookie_required(f):
    """
    Dekorator, ki zahteva veljaven piškotek. Če piškotka ni, uporabnika preusmeri na stran za prijavo.
    """
    @wraps(f)
    def decorated( *args, **kwargs):
        cookie = request.get_cookie("uporabnik")
        if cookie:
            return f(*args, **kwargs)
        return template("prijava.html",uporabnik=None, rola=None, napaka="Potrebna je prijava!")

     
        
        
    return decorated

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')



@get('/')
@cookie_required
def index():
    """
    Domača stran je stran z cenami izdelkov.
    """

    
    leta = repo.dobi_leta()
    izdelki = repo.cena_izdelkov(take=10000, leta=leta)

   
        
    return template_user('izdelki.html', izdelki=izdelki, leta=leta)
 
    
@get('/izdelki/')
@cookie_required
def izdelki():    
    
    izdelki = repo.cena_izdelkov(take=10000 )
    leta = repo.dobi_leta()
    return template_user('izdelki.html',izdelki=izdelki, leta=leta)

@post('/izdelki/')
@cookie_required
def izdelki_filter():    
    
    
    leta = repo.dobi_leta()    

    # Preverimo katera leta imamo označena
    for leto in leta:
        izbrano = request.forms.get(leto.leto)
        if izbrano is None:
            leto.izbrano = False
    take = 10000
    izdelki = repo.cena_izdelkov(take=take, leta = leta )

    return template_user('izdelki.html', izdelki=izdelki, leta=leta)

@get('/kategorije/<skip:int>/<take:int>/')
@cookie_required
def kategorije(skip, take):    
    
    kategorije = repo.kategorije_izdelkov(skip=skip, take=take )
    return template_user('kategorije.html' ,skip=skip, take=take, kategorije=kategorije)

@get('/izbrisi_izdelek/<id:int>/')
@cookie_required
def izbrisi_izdelek(id):    
    
    repo.izbrisi_gen(CenaIzdelka, id)
    izdelki = repo.cena_izdelkov(take=10000)
    leta = repo.dobi_leta()
    return template_user('izdelki.html',izdelki=izdelki, leta=leta)
   
    
    
    

@post('/prijava')
def prijava():
    """
    Prijavi uporabnika v aplikacijo. Če je prijava uspešna, ustvari piškotke o uporabniku in njegovi roli.
    Drugače sporoči, da je prijava neuspešna.
    """
    username = request.forms.get('username')
    password = request.forms.get('password')

    if not auth.obstaja_uporabnik(username):
        return template("prijava.html", napaka="Uporabnik s tem imenom ne obstaja")

    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        response.set_cookie("uporabnik", username)
        response.set_cookie("rola", prijava.role)
        
        # redirect v večino primerov izgleda ne deluje
        # redirect(url('index'))

        # Uporabimo kar template, kot v sami "index" funkciji

        leta = repo.dobi_leta()
        izdelki = repo.cena_izdelkov(take=10000, leta=leta)
        return template('izdelki.html', izdelki=izdelki, leta=leta, uporabnik=username, rola=prijava.role)
        
    else:
        return template("prijava.html", uporabnik=None, rola=None, napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.")
    
@get('/odjava')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
    """
    
    response.delete_cookie("uporabnik")
    response.delete_cookie("rola")
    
    return template('prijava.html', uporabnik=None, rola=None, napaka=None)



   

@get('/dodaj_izdelek')
def dodaj_izdelek():

    # dobimo seznam kategorij (predpostavljamo, da bo 1000 kategorj zadostovalo :))
    kategorije = repo.dobi_gen(KategorijaIzdelka, 1000, 0)
    
    # vrnemo template za dodajanje izdelka
    return template_user('dodaj_izdelek.html', izdelek = CenaIzdelkaDto(), kategorije=kategorije)

@post('/dodaj_izdelek')
def dodaj_izdelek_post():

    kategorija_id = int(request.forms.get('kategorija'))
    ime = str(request.forms.get('ime'))
    leto = request.forms.get('leto')
    cena = float(request.forms.get('cena'))

    izdelek = repo.dodaj_izdelek(Izdelek(
        ime=ime,
        kategorija=kategorija_id
    ))

    cena_izdelka = repo.dodaj_ceno_izdelka(CenaIzdelka(
        izdelek_id=izdelek.id,
        leto=leto,
        cena=cena
    ))

    
    
    redirect(url('izdelki'))
@get('/dodaj_kategorijo')
def dodaj_kategorijo():
    
    return template_user('dodaj_kategorijo.html', kategorija = KategorijaIzdelka())

@post('/dodaj_kategorijo')
def dodaj_kategorijo_post():
    oznaka = request.forms.get("kategorija")

    repo.dodaj_gen(KategorijaIzdelka(oznaka=oznaka))
    redirect(url('kategorije', skip=0, take=100))





######################################################################
# Glavni program



# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)
