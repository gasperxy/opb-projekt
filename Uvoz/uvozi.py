import pandas as pd

from Data.Database import Repo
from Modeli.Izdelki import *

repo = Repo()

def uvozi_cene(pot):

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
                oznaka=" ".join(row[1].split(" ")[1:]))
            )


  

    




#uvozi_cene("Uvoz/cene.csv")

for cena in repo.cena_izdelkov():
    print(cena)
