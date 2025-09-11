from collections import defaultdict
from datetime import datetime, time
from domain import calcular_punts

class MostrarGraficaBalance:
    """
    Cas d'ús per mostrar una gràfica dels moviments.
    Converteix els moviments en punts (datetime, balance, banc)
    i envia a la UI les dades de la gràfica.
    """

    def __init__(self, ui):
        self._ui = ui

    def execute(self, moviments):
        
        sorted_punts = calcular_punts(moviments)
        dades = {
            "punts": sorted_punts,
            "etiqueta_x": "Data/Hora",
            "etiqueta_y": "Balanç",
        }
        for d in dades["punts"]:
            print(d)
        self._ui.mostrar_grafica(dades)
        