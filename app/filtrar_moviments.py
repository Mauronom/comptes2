from domain.moviment import Moviment

class FiltrarMoviments:
    def __init__(self, repositori, ui):
        self._repositori = repositori
        self._ui = ui

    def execute(self, text: str):
        """Filtra els moviments i actualitza la UI."""
        moviments = self._repositori.obtenir_tots()
        self._ui.print(len(moviments))
        text = (text or "").lower()
        if text:
            moviments = [
                m for m in moviments
                if text in m.concepte.lower()
            ]

        self._ui.mostrar_moviments(moviments)
