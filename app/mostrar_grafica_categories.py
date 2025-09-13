from collections import defaultdict
from datetime import datetime, time
from domain import calcular_punts, Moviment
from decimal import Decimal

class MostrarGraficaCategories:
    """
    Cas d'ús per mostrar una gràfica dels moviments.
    Converteix els moviments en punts (datetime, balance, banc)
    i envia a la UI les dades de la gràfica.
    """

    def __init__(self, ui):
        self._ui = ui

    def execute(self, moviments):
        movs = Moviment.clone_list(moviments)
        despeses = {}
        estalvi = Decimal(0.0)
        for m in movs:
            estalvi += m.import_
            key = m.categoria
            if key not in despeses:
                despeses[key] = Decimal(0.0)
            despeses[key] += m.import_
        for d in despeses:
            despeses[d] = float(despeses[d])
        self._ui.mostrar_grafica_categories(despeses, float(estalvi))
        