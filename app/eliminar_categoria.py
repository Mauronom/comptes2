class EliminarCategoria:
    """
    Cas d'ús per eliminar una categoria existent.
    Rep el nom de la categoria i la elimina del repositori.
    """
    
    def __init__(self, repositori_categories):
        self._repositori_categories = repositori_categories

    def execute(self, nom_categoria):
        """
        Executa el cas d'ús per eliminar una categoria.
        
        Args:
            nom_categoria (str): El nom de la categoria a eliminar
            
        Returns:
            bool: True si la categoria s'ha eliminat correctament, False si no existia
        """
        return self._repositori_categories.delete(nom_categoria)