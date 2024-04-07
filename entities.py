from typing import Any, Dict, NamedTuple, Tuple


class Lieu:
    _ALL: Dict[str, "Lieu"] = {}

    def __init__(self, nom: str, coords: Tuple[float, float]):
        self._nom = nom
        self._coords = coords
        self._ALL[nom] = self
    
    def __repr__(self) -> str:
        return f"Lieu: {self.nom} - {self.coords}"

    @property
    def nom(self) -> str:
        return self._nom
    
    @property
    def coords(self) -> Tuple[float, float]:
        return self._coords
    
    @classmethod
    def from_name(cls, nom: str) -> "Lieu":
        return cls._ALL.get(nom)

    def to_fullcalendar(self):
        return {
            "id": self.nom,
            "title": self.nom
        }


class Evenement(NamedTuple):
    jour: int
    debut: str
    fin: str
    nom: str
    description: str
    lieu: Lieu

    def __key(self):
        return (self.jour, self.nom, self.lieu.nom)
    
    def __hash__(self):
        return hash(self.__key())
    
    def __eq__(self, other):
        if isinstance(other, Evenement):
            return self.key() == other.key()
        return NotImplemented

    @staticmethod
    def create(
        jour, debut, fin, nom, description, lieu: str
    ):
        return Evenement(
            jour, debut, fin, nom, description, Lieu.from_name(lieu)
        )

    def to_fullcalendar(self) -> Dict[str, Any]:
        return {
            "start": f"0001-01-{self.jour:02d}T{self.debut}",
            "end": f"0001-01-{self.jour:02d}T{self.fin}",
            "title": self.nom,
            "resourceId": self.lieu.nom
        }
