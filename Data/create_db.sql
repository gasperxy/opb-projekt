CREATE table KategorijaIzdelka(
    id SERIAL PRIMARY KEY,
    oznaka TEXT UNIQUE
);

CREATE table Izdelek(
    id SERIAL PRIMARY KEY,
    ime TEXT UNIQUE, 
    kategorija BIGINT REFERENCES KategorijaIzdelka(id)
);

CREATE TABLE CenaIzdelka(
    id SERIAL PRIMARY KEY,
    izdelek_id BIGINT REFERENCES Izdelek(id),
    leto DATE, 
    cena FLOAT

);