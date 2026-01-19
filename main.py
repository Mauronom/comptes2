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
from app import MostrarCategories
from app import AfegirCategoria
from app import EditarCategoria
from app import EliminarCategoria

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
    cas_us_mostrar_categories = MostrarCategories(repositori_cats, ui)
    cas_us_afegir_categoria = AfegirCategoria(repositori_cats, ui)
    cas_us_editar_categoria = EditarCategoria(repositori_cats, ui)
    cas_us_eliminar_categoria = EliminarCategoria(repositori_cats, ui)
    ui.set_casos_us(cas_us_grafica_balance, cas_us_grafica_imports, cas_us_filtrar_moviments, cas_us_grafica_categories, cas_us_mostrar_categories, cas_us_afegir_categoria, cas_us_editar_categoria, cas_us_eliminar_categoria)
    
    # Ara sense moviment hardcodejat!
    cas_us_inici = IniciarAplicacio(repositori, ui, repositori_cats, repositori_config)
    cas_us_inici.execute()