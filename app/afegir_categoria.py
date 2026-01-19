class AfegirCategoria:
    """
    Cas d'ús per afegir una nova categoria.
    Rep una categoria i les seves paraules clau i les desa al repositori.
    """
    
    def __init__(self, repositori_categories):
        self._repositori_categories = repositori_categories

    def execute(self, nom_categoria, paraules_clau):
        """
        Executa el cas d'ús per afegir una nova categoria.
        
        Args:
            nom_categoria (str): El nom de la nova categoria
            paraules_clau (list): Llista de paraules clau associades a la categoria
        """
        self._repositori_categories.save(nom_categoria, paraules_clau)