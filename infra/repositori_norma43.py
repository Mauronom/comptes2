import os
from domain import Moviment
from domain import RepositoriMoviments
from norma43parser import Norma43Parser, DateFormat

class RepositoriMovimentsNorma43(RepositoriMoviments):
    """
    Repositori que llegeix moviments de fitxers Norma 43 utilitzant norma43parser.
    """

    def __init__(self, directori="infra/dades"):
        self._directori = directori
        self._parser = Norma43Parser(DateFormat.ENGLISH)  # Utilitza AAAAMMDD
        self.moviments = self.llegir_moviments()

    def obtenir_tots(self):
        return self.moviments.copy()

    def enriquir(self,movs):
        self.moviments.extend(movs)
        
    def llegir_moviments(self):
        moviments = []
        for fitxer in os.listdir(self._directori):
            if fitxer.lower().endswith((".n43", ".txt")):
                banc = os.path.splitext(fitxer)[0]
                path = os.path.join(self._directori, fitxer)
                with open(path, "r", encoding="latin-1", errors="ignore") as f:
                    contents = f.read()
                doc = self._parser.parse(contents)
                for account in doc.accounts:
                    for line in account.movement_lines:
                        moviments.append(
                            Moviment(
                                line.transaction_date,
                                line.extra_information[0].replace('      ',' ').strip(),
                                float(line.amount),
                                line.balance,
                                banc
                            )
                        )
        return sorted(moviments, key=lambda m: m.data)
