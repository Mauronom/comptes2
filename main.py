from infra import RepositoriMovimentsNorma43
from infra import UITextualGrafica
from infra import UIMatplotlib
from infra import UIBokeh
from app import IniciarAplicacio
from app import MostrarGraficaBalance
from app import MostrarGraficaImports
from app import FiltrarMoviments
from domain import Moviment
import datetime

if __name__ == "__main__":
    repositori = RepositoriMovimentsNorma43(directori="infra/dades")
    # ui_grafica = UIMatplotlib()
    ui_grafica = UIBokeh()
    ui = UITextualGrafica(repositori)
    cas_us_grafica_balance = MostrarGraficaBalance(ui_grafica)
    cas_us_grafica_imports = MostrarGraficaImports(ui_grafica)
    cas_us_filtrar_moviments = FiltrarMoviments(repositori,ui)
    ui.set_casos_us(cas_us_grafica_balance, cas_us_grafica_imports, cas_us_filtrar_moviments)
    # cas_us_inici = IniciarAplicacio(repositori, ui)
    cas_us_inici = IniciarAplicacio(repositori, ui, extra_moves=[Moviment(
                    data=datetime.date(2024, 8, 1),
                    concepte="SIALP PIES",
                    import_=0,
                    balance=17000,
                    banc="SIALP_PIAS"
                )])
    cas_us_inici.execute()
