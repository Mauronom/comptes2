from abc import ABC, abstractmethod

class RepositoriMoviments(ABC):
    """
    Interfície base per a repositoris de moviments.
    """

    @abstractmethod
    def obtenir_tots(self):
        """Retorna una llista de Moviment"""
        pass
