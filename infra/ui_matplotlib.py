import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import defaultdict

class UIMatplotlib:
    def mostrar_grafica(self, dades: dict):
        """
        Rep un diccionari amb:
          - punts: [(datetime, balance, banc), ...]
          - etiqueta_x: str
          - etiqueta_y: str
        i dibuixa una línia per a cada banc.
        """
        punts = dades["punts"]
        etiqueta_x = dades["etiqueta_x"]
        etiqueta_y = dades["etiqueta_y"]

        if not punts:
            print("No hi ha dades per mostrar")
            return

        # Agrupar punts per banc
        per_banc = defaultdict(list)
        for dt, balance, banc in punts:
            per_banc[banc].append((dt, balance))

        plt.figure(figsize=(10, 5))

        for banc, punts_banc in per_banc.items():
            punts_banc.sort(key=lambda p: p[0])  # ordenar per data/hora
            x = [p[0] for p in punts_banc]
            y = [p[1] for p in punts_banc]
            plt.plot(x, y, marker="o", linestyle="-", label=banc)

        # Format de l’eix temporal
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
        plt.gcf().autofmt_xdate()

        plt.xlabel(etiqueta_x)
        plt.ylabel(etiqueta_y)
        plt.title("Evolució del balanç per banc")
        plt.legend()
        plt.grid(True)
        plt.show()
