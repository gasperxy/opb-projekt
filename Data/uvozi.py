import pandas as pd
from pandas import DataFrame

from Data.Database import Repo
from Data.Modeli import *
from Data.Services import AuthService
from typing import Dict
from re import sub
import dataclasses


# Vse kar delamo z bazo se nahaja v razredu Repo.
repo = Repo()
auth = AuthService(repo)



def uvozi_cene(pot):
    """
    Uvozimo csv s cenami izdelkov v bazo.
    Pri tem predpostavljamo, da imamo tabele že ustvarjene. 
    Vsako vrstico posebaj še obdelamo, da v bazi dobimo željeno strukturo. Uporabimo
    razred Repo za klic funkcij za uvoz v bazo.
    """

    df = pd.read_csv(pot, sep=";",skiprows=[0], encoding="Windows-1250")

    # Iz stolpcev razberemo katera leta imamo
    leta = dict()
    for i, c in enumerate(df.columns):

        # Če je zadni del številka ga obravnavamo kot leto
        if c.split(" ")[-1].isdigit():
            leta[i] = int(c.split(" ")[-1])

    kategorija = KategorijaIzdelka()
    for row in df.itertuples():

       
        if row[1].startswith("..."):
            # Vrstica je izdelek


            izdelek = repo.dodaj_izdelek(
                Izdelek(
                 ime=row[1].replace("...", ""),
                 kategorija=kategorija.id)
            )

            # Dodamo še vse cene izdelka
            for i, leto in leta.items():
                try:
                    cena = float(row[i+1])
                    repo.dodaj_ceno_izdelka(CenaIzdelka(
                        izdelek_id=izdelek.id,
                        leto=leto,
                        cena=cena
                    ))

                except ValueError:
                    pass
               

        else:
            # Vrstica je kategorija
            

            kategorija = repo.dodaj_kategorijo(
                KategorijaIzdelka( 
                    oznaka= " ".join(row[1].split(" ")[1:]))
            )


def uvozi_csv(pot, ime):
    """
    Uvozimo csv v bazo brez večjih posegov v podatke.
    Ustvarimo pandasov DataFrame ter nato z generično metodo ustvarimo ter
    napolnimo tabelo v postgresql bazi.
    """
    df = pd.read_csv(pot, sep=";",skiprows=[0], encoding="Windows-1250")

    # Zamenjamo pomišljaje z prazno vrednostjo
    df.replace(to_replace="-", value="", inplace=True)

    # Naredimo tabelo z dodatnim serial primary key stolpcem
    repo.df_to_sql_create(df, ime, add_serial=True, use_camel_case=True)

    # uvozimo podatke v to isto tabelo
    repo.df_to_sql_insert(df, ime, use_camel_case=True)



def uvozi_opsi(pot, ime):
    """
    Uvozimo csv v bazo brez večjih posegov v podatke.
    Ustvarimo pandasov DataFrame ter nato z generično metodo ustvarimo ter
    napolnimo tabelo v postgresql bazi.
    """
    df = pd.read_csv(pot, sep=",", encoding='utf-16le')

    
    # Vzamemo le prvih 500000 vrstic (zardi hitrosti inserta, itd.)
    df = df.iloc[:500000]   

    # Naredimo tabelo z dodatnim serial primary key stolpcem
    repo.df_to_sql_create(df, ime, add_serial=True, use_camel_case=True)

    # uvozimo podatke v to isto tabelo
    repo.df_to_sql_insert(df, ime, use_camel_case=True)



# Uvozimo csv, ki ima kar veliko vrstic (za testiranje izdelave indexov)
pot_opsi = "/Users/gasper/Documents/fmf/opbpodatki/opsiprs.csv"

uvozi_opsi(pot_opsi, "podjetja")







# Primeri uporabe. Zakomentiraj določene vrstice, če jih ne želiš izvajat!
    

pot = "Data/cene.csv"



# Uvozi csv s cenami izdelkov v ločene (in povezane) entitete
# Tabele morajo biti prej ustvarjene, da zadeva deluje

# uvozi_cene(pot)

# Uvozi csv s cenami, le da tokar uvozi le eno tabelo, ki jo
# predhodno še ustvari, če ne obstaja.

# uvozi_csv(pot, "NovaTabela")

# primer ročnega dodajanja uporabnikov

uporabnik1 = auth.dodaj_uporabnika("gasper", "user", "gasper")

uporabnik = auth.dodaj_uporabnika("admin", "admin", "admin")





# S pomočjo generične metode dobimo seznam izdelkov in kategorij
# Privzete nastavi

# Dobimo prvih 100 izdelkov
izdelki = repo.dobi_gen(Izdelek, skip=0, take=100)

t = repo.dobi_gen(IzdelekDto)

# Dobimo prvih 10 kategorij
kategorije = repo.dobi_gen(KategorijaIzdelka)

# Dodamo novo kategorijo

nova_kategorija = KategorijaIzdelka(
    oznaka="Nova kategorija"
)

repo.dodaj_gen(nova_kategorija)

# vrednost nova_kategorija.id je sedaj določen na podlagi
# serial vrednosti iz baze in jo lahko uporabimo naprej.


# Dodamo nov izdelek v to kategorijo
novi_izdelek = Izdelek(
    ime = 'Novi izdelek',
    kategorija=nova_kategorija.id
)
repo.dodaj_gen(novi_izdelek)


# Dobimo izdelek z idjem 832
izdelek = repo.dobi_gen_id(Izdelek, 832)

# izdelku spremenimo ime in ga posodobimo v bazi
izdelek.ime += " spremenjeno ime"
repo.posodobi_gen(izdelek)



# spremenimo seznam izdelkov in ga shranimo v bazo

for i in izdelki:
    i.ime = f'({i.ime})'

repo.posodobi_list_gen(izdelki)


