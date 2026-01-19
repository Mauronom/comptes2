class MostrarCategories:
    """
    Cas d'ús per mostrar la llista de categories.
    Obté totes les categories del repositori i les envia a la UI.
    """
    
    def __init__(self, repositori_categories, ui):
        self._repositori_categories = repositori_categories
        self._ui = ui

    def execute(self):
        """
        Executa el cas d'ús per obtenir i mostrar totes les categories.
        """
        categories = self._repositori_categories.get_all()
        self._ui.mostrar_categories(categories)