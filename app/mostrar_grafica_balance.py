from collections import defaultdict
from datetime import datetime, time
from domain import calcular_punts, Moviment

class MostrarGraficaBalance:
    """
    Cas d'ús per mostrar una gràfica dels moviments.
    Converteix els moviments en punts (datetime, balance, banc)
    i envia a la UI les dades de la gràfica.
    """

    def __init__(self, ui):
        self._ui = ui

    def execute(self, moviments):
        movs = Moviment.clone_list(moviments)
        sorted_punts = calcular_punts(movs)
        dades = {
            "punts": sorted_punts,
            "etiqueta_x": "Data/Hora",
            "etiqueta_y": "Balanç",
        }
        self._ui.mostrar_grafica(dades)
        