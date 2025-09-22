from infra import RepositoriMovimentsNorma43
from infra import RepositoriCategoria
from infra import UIBokeh
from infra import UIFreeSimpleGUI
from infra import JsonConfigMovimentsFicticisRepo
from app import IniciarAplicacio
from app import MostrarGraficaBalance
from app import MostrarGraficaImports
from app import MostrarGraficaCategories
from app import FiltrarMoviments

if __name__ == "__main__":
    repositori = RepositoriMovimentsNorma43()
    repositori_cats = RepositoriCategoria(directori="infra/dades")
    repositori_config = JsonConfigMovimentsFicticisRepo("infra/dades/config.json")
    ui_grafica = UIBokeh()
    ui = UIFreeSimpleGUI(repositori, repositori_cats)
    
    cas_us_grafica_balance = MostrarGraficaBalance(ui_grafica)
    cas_us_grafica_imports = MostrarGraficaImports(ui_grafica)
    cas_us_grafica_categories = MostrarGraficaCategories(ui_grafica)
    cas_us_filtrar_moviments = FiltrarMoviments(repositori, ui)
    ui.set_casos_us(cas_us_grafica_balance, cas_us_grafica_imports, cas_us_filtrar_moviments, cas_us_grafica_categories)
    
    # Ara sense moviment hardcodejat!
    cas_us_inici = IniciarAplicacio(repositori, ui, repositori_cats, repositori_config)
    cas_us_inici.execute()