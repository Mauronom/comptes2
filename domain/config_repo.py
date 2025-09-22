from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass

@dataclass
class ReglaMovimentFictici:
    patrons: List[str]
    concepte_desti: str
    banc_desti: str
    invertir_import: bool = True

class ConfigMovimentsFicticisRepo(ABC):
    @abstractmethod
    def get_regles(self) -> List[ReglaMovimentFictici]:
        pass
    
    @abstractmethod
    def get_moviments_inicials(self) -> List:
        pass