import os
from domain import Moviment
from domain import RepositoriMoviments

class RepositoriMovimentsNorma43(RepositoriMoviments):
    """
    Repositori que llegeix moviments de fitxers Norma 43 utilitzant norma43parser.
    """

    def __init__(self):
        from norma43parser import Norma43Parser, DateFormat
        self._parser = Norma43Parser(DateFormat.ENGLISH)  # Utilitza AAAAMMDD
        self.moviments = []

    def set_directori(self, directori):
        self.directori = directori
        self.moviments = self.llegir_moviments(self.directori)


    def obtenir_tots(self,):
        """
        Llegeix i retorna tots els moviments del directori passat per paràmetre.
        """
        return Moviment.clone_list(self.moviments)

    def enriquir(self, movs):
        self.moviments.extend(movs)

    def save(self, movs):
        self.moviments = Moviment.clone_list(movs)

    def llegir_moviments(self, directori):
        moviments = []
        for fitxer in os.listdir(directori):
            if fitxer.lower().endswith((".n43")):
                banc = os.path.splitext(fitxer)[0]
                path = os.path.join(directori, fitxer)
                with open(path, "r", encoding="latin-1", errors="ignore") as f:
                    contents = f.read()
                doc = self._parser.parse(contents)
                for account in doc.accounts:
                    for line in account.movement_lines:
                        moviments.append(
                            Moviment(
                                line.transaction_date,
                                line.extra_information[0].replace('      ', ' ').strip(),
                                float(line.amount),
                                line.balance,
                                banc
                            )
                        )
        return sorted(moviments, key=lambda m: m.data)
