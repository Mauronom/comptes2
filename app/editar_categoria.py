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
        Demana a la UI el nom de la categoria i les paraules clau.
        """
        # Demanar a la UI el nom de la categoria a editar
        nom_categoria = self._ui.input_popup("Editar categoria:", "Editar Categoria")

        # Si no es proporciona un nom de categoria, no fem res
        if not nom_categoria:
            return

        # Demanar a la UI les noves paraules clau
        paraules_clau_str = self._ui.input_popup("Editar paraules clau:", "Editar Paraules Clau")

        # Processar la cadena de paraules clau en una llista
        if paraules_clau_str:
            paraules_clau = [p.strip() for p in paraules_clau_str.split(",") if p.strip()]
        else:
            paraules_clau = []

        # Desar la categoria actualitzada al repositori
        self._repositori_categories.save(nom_categoria, paraules_clau)

        # Mostrar missatge de confirmació a la UI
        self._ui.mostrar_popup("Èxit", f"S'ha editat la categoria '{nom_categoria}' amb {len(paraules_clau)} paraules clau.")