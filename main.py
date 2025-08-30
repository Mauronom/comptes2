from infra import RepositoriMovimentsNorma43
from infra import UITextualGrafica
from infra import UIMatplotlib
from infra import UIBokeh
from app import IniciarAplicacio
from app import MostrarGrafica
from app import FiltrarMoviments
from domain import Moviment
import datetime
from decimal import Decimal

if __name__ == "__main__":
    repositori = RepositoriMovimentsNorma43(directori="infra/dades")
    # ui_grafica = UIMatplotlib()
    ui_grafica = UIBokeh()
    ui = UITextualGrafica(repositori)
    cas_us_grafica = MostrarGrafica(ui_grafica)
    cas_us_filtrar_moviments = FiltrarMoviments(repositori,ui)
    ui.set_casos_us(cas_us_grafica, cas_us_filtrar_moviments)
    # cas_us_inici = IniciarAplicacio(repositori, ui)
    cas_us_inici = IniciarAplicacio(repositori, ui, extra_moves=[Moviment(
                    data=datetime.date(2024, 8, 1),
                    concepte="SIALP PIES",
                    import_=Decimal(17000),
                    balance=Decimal(17000),
                    banc="SIALP_PIAS"
                )])
    cas_us_inici.execute()
