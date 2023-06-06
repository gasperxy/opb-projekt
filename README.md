# opb-projekt

## Namestitev virtualnega okolja

Ustvarimo okolje: 

`python3 -m venv env`

Aktiviramo okolje

 `source env/bin/activate`

Naložimo potrebne knjižnjice

 `env/bin/pip3 install -r requirenments.txt`

 **Pozor:** Zgornji ukazi se lahko razlikujejo med razlinimi okolji (windows, mac, linux), zato je najboljše, da si virtualna okolja nahitro ogledate recimo na [virtualna okolja](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/).

 ## Modeli in vmesnik za bazo

 **Model** je python razdred, ki opisuje entiteto oziroma tabelo v bazi. Zaradi lažje posplošitve so ključni modeli narejeni za vsako tabelo v bazi, pri tem pa pazimo, da so imena objektov in njihovih atributov usklajena z imeni tabel ter njihovimi stolpci (sql ni case sensitive!).

 Modele lahko predstavimo z navadnim python razredom, lahko pa si pomagamo z uporabno knjižnjico **dataclasses** in razred opremimo z dataclass anotacijo. Oglejte si recimo datoteko [Modeli.py](Data/Modeli.py).

 Python vmesnik za bazo sem implementiral v datoteki [Database.py](Data/Database.py) in vsebuje funkcije za:
 * **Generične metode** za  SELECT, UPDATE in INSERT
 * Delo z pandas DataFrame objektom (create table, insert)
 * Nekaj NE generičlnih metod za delo z tabelami.

Njegovo uporabo lahko pogledate v datoteki [uvozi.py](Data/uvozi.py).

## Spletni dostop
* [![bottle.py](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gasperxy/opb-projekt/main?urlpath=proxy/8080/) Aplikacija `bottle.py`