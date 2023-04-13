from dataclasses import dataclass, field

@dataclass
class Izdelek:
    id: int = field(default=0)
    ime: str = field(default="")
    kategorija: int = field(default=0)

@dataclass
class IzdelekDto:
    id: int = field(default=0)
    ime: str = field(default="")
    oznaka: str = field(default="")



@dataclass
class KategorijaIzdelka:
    id: int = field(default=0)
    oznaka: str = field(default="")

@dataclass
class CenaIzdelka:
    id: int = field(default=0)
    izdelek_id : int = field(default=0)
    leto : str = field(default="")
    cena : float = field(default=0)

@dataclass
class CenaIzdelkaDto:
    id: int = field(default=0)
    izdelek_id : int = field(default=0)
    izdelek_ime : str = field(default="")
    izdelek_oznaka : str = field(default="")
    leto : str = field(default="")
    cena : float = field(default=0)







