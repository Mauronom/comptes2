from collections import defaultdict
from datetime import datetime, time
from domain import calcular_punts, Moviment

class MostrarGraficaImports:
    """
    Cas d'ús per mostrar una gràfica dels moviments.
    Converteix els moviments en punts (datetime, import_, banc)
    i envia a la UI les dades de la gràfica.
    """

    def __init__(self, ui):
        self._ui = ui

    def execute(self, moviments):
        movs = Moviment.clone_list(moviments)
        movs.sort(key=lambda m: (m.data, m.banc))
        totals = {}
        for m in movs:
            if m.banc not in totals:
                totals[m.banc] = 0
            totals[m.banc] += m.import_
            m.balance = totals[m.banc]
            m.import_ = m.import_
        sorted_punts = calcular_punts(movs)
        dades = {
            "punts": sorted_punts,
            "etiqueta_x": "Data/Hora",
            "etiqueta_y": "Import Acumulat",
        }
        self._ui.mostrar_grafica(dades)
    
        