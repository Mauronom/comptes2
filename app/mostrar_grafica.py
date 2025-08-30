from collections import defaultdict
from datetime import datetime, time

class MostrarGrafica:
    """
    Cas d'ús per mostrar una gràfica dels moviments.
    Converteix els moviments en punts (datetime, balance, banc)
    i envia a la UI les dades de la gràfica.
    """

    def __init__(self, ui):
        self._ui = ui

    def execute(self, moviments):
        
        # Comptador d’hores per cada (data, banc)
        comptadors = defaultdict(int)
        punts = []
        bancs = []
        for m in moviments:
            if m.banc not in bancs:
                bancs.append(m.banc)
            hora = comptadors[(m.data, m.banc)]
            dt = datetime.combine(m.data, time(hour=hora))
            punts.append((dt, m.balance, m.banc))
            comptadors[(m.data, m.banc)] += 1
        sorted_punts = sorted(punts, key=lambda p: (p[0], p[2]))
        # Afegir punts totals per data
        per_data = defaultdict(float)
        aux = {}
        for b in bancs:
            aux[b] = 0
        per_data_i = [aux]
        dt_ant = None
        for dt, balance, banc in sorted_punts:
            if dt != dt_ant:
                aux = {}
                for b in bancs:
                    aux[b] = 0
                aux['data'] = dt
                per_data_i.append(aux)
                dt_ant = dt
            per_data_i[len(per_data_i)-1][banc] += balance
        # per_data_i[len(per_data_i)-1]['Total'] = sum(per_data_i[len(per_data_i)-1][b] for b in bancs)
        i = 1
        for e in per_data_i[1:]:
            for b in bancs:
                if e[b]==0:
                    e[b] = per_data_i[i-1][b]
            e["Total"] = sum(e[b] for b in bancs)
            sorted_punts.append((e['data'], e["Total"], "Total"))
            i = i+1
        
        sorted_punts = sorted(sorted_punts, key=lambda p: (p[0], p[2]))
        dades = {
            "punts": sorted_punts,
            "etiqueta_x": "Data/Hora",
            "etiqueta_y": "Balanç",
        }
        for d in dades["punts"]:
            print(d)
        self._ui.mostrar_grafica(dades)
        dades = {
            "punts": sorted_punts,
            "etiqueta_x": "Data/Hora",
            "etiqueta_y": "Import Acumulat",
        }
        self._ui.mostrar_grafica(dades)
