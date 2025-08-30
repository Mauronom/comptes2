from domain.moviment import Moviment
import datetime
from decimal import Decimal, ROUND_HALF_UP

class IniciarAplicacio:
    def __init__(self, repositori_moviments, ui, extra_moves=[]):
        self._repositori = repositori_moviments
        self._ui = ui
        self.extra_moves = extra_moves
        

    def afegir_moviments_ficticis(self, moviments):
        movs = self.extra_moves.copy()
        for m in moviments:
            if "PLAN UNI SEGUR" in m.concepte or "PLAN AHORRO 5 SIALP" in m.concepte or "CI PIAS" in m.concepte:
                movs.append(Moviment(
                    data=m.data,
                    concepte="SIALP PIES",
                    import_=Decimal(-m.import_),
                    balance=Decimal(-m.import_).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) if not movs else (Decimal(movs[-1].balance) + Decimal(-m.import_)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                    banc="SIALP_PIAS"
                ))
        print(len(movs))
        return movs
        
    def execute(self):
        """
        Obté els moviments del repositori i actualitza la UI.
        """
        moviments = self._repositori.obtenir_tots()
        movs = self.afegir_moviments_ficticis(moviments)
        self._repositori.enriquir(movs)
        moviments = self._repositori.obtenir_tots()
        moviments = sorted(moviments, key=lambda m: (m.data,m.banc))

        # La UI hauria de tenir un mètode mostrar_moviments
        self._ui.mostrar_moviments(moviments)
        # Si és una UI Textual, llavors cridem run() per iniciar l'app
        if hasattr(self._ui, "run"):
            self._ui.run()
