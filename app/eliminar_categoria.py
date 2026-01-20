class EliminarCategoria:
    """
    Cas d'ús per eliminar una categoria existent.
    Rep el nom de la categoria i la elimina del repositori.
    També pot interactuar amb la UI per obtenir les dades de l'usuari.
    """

    def __init__(self, repositori_categories, ui):
        self._repositori_categories = repositori_categories
        self._ui = ui

    def execute(self):
        """
        Executa el cas d'ús per eliminar una categoria.
        Demana a la UI que l'usuari seleccioni una categoria i confirmeu l'acció.

        Returns:
            bool: True si la categoria s'ha eliminat correctament, False si no existia o si es va cancel·lar
        """
        # Obtenir totes les categories disponibles
        categories = self._repositori_categories.get_all()

        # Si no hi ha categories, no podem eliminar res
        if not categories:
            self._ui.mostrar_popup("Error", "No hi ha categories per eliminar.")
            return False

        # Demanar a la UI que l'usuari seleccioni una categoria
        nom_categoria = self._ui.seleccionar_categoria(list(categories.keys()), "Selecciona la categoria a eliminar:")

        # Si no es selecciona cap categoria, no fem res
        if not nom_categoria:
            return False

        # Demanar confirmació a l'usuari
        confirmacio = self._ui.confirmar_accio(f"Segur que vol eliminar la categoria '{nom_categoria}'?")

        # Si l'usuari no confirma, no fem res
        if not confirmacio:
            self._ui.mostrar_popup("Cancel·lat", f"S'ha cancel·lat l'eliminació de la categoria '{nom_categoria}'.")
            return False

        # Intentar eliminar la categoria del repositori
        resultat = self._repositori_categories.delete(nom_categoria)

        # Mostrar missatge de confirmació a la UI
        if resultat:
            self._ui.mostrar_popup("Èxit", f"S'ha eliminat la categoria '{nom_categoria}' correctament.")
        else:
            self._ui.mostrar_popup("Error", f"No s'ha pogut eliminar la categoria '{nom_categoria}'.")

        # Actualitzar la vista de categories si l'eliminació va ser exitosa
        if resultat:
            self._ui.actualitzar_categories()

        return resultat