class AfegirCategoria:
    """
    Cas d'ús per afegir una nova categoria.
    Rep una categoria i les seves paraules clau i les desa al repositori.
    També pot interactuar amb la UI per obtenir les dades de l'usuari.
    """

    def __init__(self, repositori_categories, ui):
        self._repositori_categories = repositori_categories
        self._ui = ui

    def execute(self):
        """
        Executa el cas d'ús per afegir una nova categoria.
        Demana a la UI el nom de la categoria i les paraules clau.
        """
        # Demanar a la UI el nom de la nova categoria
        nom_categoria = self._ui.input_popup("Nom de la nova categoria:", "Nova Categoria")

        # Si no es proporciona un nom de categoria, no fem res
        if not nom_categoria:
            return

        # Demanar a la UI les paraules clau
        paraules_clau_str = self._ui.input_popup("Paraules clau separades per comes:", "Paraules Clau")

        # Processar la cadena de paraules clau en una llista
        if paraules_clau_str:
            paraules_clau = [p.strip() for p in paraules_clau_str.split(",") if p.strip()]
        else:
            paraules_clau = []

        # Desar la nova categoria al repositori
        self._repositori_categories.save(nom_categoria, paraules_clau)

        # Mostrar missatge de confirmació a la UI
        self._ui.mostrar_popup("Èxit", f"S'ha afegit la categoria '{nom_categoria}' amb {len(paraules_clau)} paraules clau.")

        # Actualitzar la vista de categories
        self._ui.actualitzar_categories()