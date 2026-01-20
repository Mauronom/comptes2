class EditarCategoria:
    """
    Cas d'ús per editar una categoria existent.
    Rep una categoria i les seves noves paraules clau i les desa al repositori.
    També pot interactuar amb la UI per obtenir les dades de l'usuari.
    """

    def __init__(self, repositori_categories, ui):
        self._repositori_categories = repositori_categories
        self._ui = ui

    def execute(self):
        """
        Executa el cas d'ús per editar una categoria.
        Demana a la UI que l'usuari seleccioni una categoria i llavors les paraules clau.
        """
        # Obtenir totes les categories disponibles
        categories = self._repositori_categories.get_all()

        # Si no hi ha categories, no podem editar res
        if not categories:
            self._ui.mostrar_popup("Error", "No hi ha categories per editar.")
            return

        # Demanar a la UI que l'usuari seleccioni una categoria
        nom_categoria = self._ui.seleccionar_categoria(list(categories.keys()), "Selecciona la categoria a editar:")

        # Si no es selecciona cap categoria, no fem res
        if not nom_categoria:
            return

        # Demanar a la UI les noves paraules clau
        # Si la categoria ja existeix, pre-omplim amb les paraules clau actuals
        default_paraules = ""
        if nom_categoria in categories:
            default_paraules = ", ".join(categories[nom_categoria])

        paraules_clau_str = self._ui.input_popup("Editar paraules clau:", "Editar Paraules Clau", default_text=default_paraules)

        # Processar la cadena de paraules clau en una llista
        if paraules_clau_str:
            paraules_clau = [p.strip() for p in paraules_clau_str.split(",") if p.strip()]
        else:
            paraules_clau = []

        # Desar la categoria actualitzada al repositori
        self._repositori_categories.save(nom_categoria, paraules_clau)

        # Mostrar missatge de confirmació a la UI
        self._ui.mostrar_popup("Èxit", f"S'ha editat la categoria '{nom_categoria}' amb {len(paraules_clau)} paraules clau.")

        # Actualitzar la vista de categories
        self._ui.actualitzar_categories()