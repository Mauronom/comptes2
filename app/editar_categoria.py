class EditarCategoria:
    """
    Cas d'ús per editar una categoria existent.
    Rep una categoria i les seves noves paraules clau i les desa al repositori.
    """
    
    def __init__(self, repositori_categories):
        self._repositori_categories = repositori_categories

    def execute(self, nom_categoria, paraules_clau):
        """
        Executa el cas d'ús per editar una categoria.
        
        Args:
            nom_categoria (str): El nom de la categoria a editar
            paraules_clau (list): Llista de paraules clau actualitzades per la categoria
        """
        self._repositori_categories.save(nom_categoria, paraules_clau)