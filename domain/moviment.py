from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Union

@dataclass
class Moviment:
    data: date
    concepte: str
    import_: Union[Decimal, float, int, str]
    balance: Union[Decimal, float, int, str]
    banc: str
    categoria: str = "altres"

    def __post_init__(self):
        # Convertir automàticament a Decimal
        if not isinstance(self.import_, Decimal):
            self.import_ = Decimal(str(self.import_))
        
        if not isinstance(self.balance, Decimal):
            self.balance = Decimal(str(self.balance))
            
    def clone(self):
        return Moviment(
            data=self.data,
            concepte=self.concepte,
            import_=self.import_,
            balance=self.balance,
            banc=self.banc,
            categoria=self.categoria
        )
    
    @staticmethod
    def clone_list(moviments):
        return [m.clone() for m in moviments]


def assignar_categories_a_moviments(moviments, categories_repo):
    """
    Assigna categories als moviments segons les paraules clau del repositori de categories.

    Args:
        moviments: Llista de moviments a categoritzar
        categories_repo: Repositori de categories que conté les paraules clau

    Returns:
        Llista de moviments amb les categories assignades
    """
    cats = categories_repo.get_all()
    moviments_resultats = []

    for m in moviments:
        # Crear una còpia del moviment per no modificar l'original
        moviment_copia = m.clone()

        # Buscar coincidències amb les paraules clau de les categories
        categoria_assignada = "altres"  # Valor per defecte

        for cat in cats.keys():
            texts = cats[cat]
            for t in texts:
                if t.lower() in moviment_copia.concepte.lower():
                    categoria_assignada = cat
                    break
            if categoria_assignada != "altres":
                break

        # Assignar la categoria trobada (o "altres" si no hi ha coincidències)
        moviment_copia.categoria = categoria_assignada
        moviments_resultats.append(moviment_copia)

    return moviments_resultats


