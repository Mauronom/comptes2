from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Union

@dataclass
class Moviment:
    data: date
    concepte: str
    import_: Union[Decimal, float, int, str]
    balance: Union[Decimal, float, int, str]
    banc: str
    categoria: str = "altres"

    def __post_init__(self):
        # Convertir automàticament a Decimal
        if not isinstance(self.import_, Decimal):
            self.import_ = Decimal(str(self.import_))
        
        if not isinstance(self.balance, Decimal):
            self.balance = Decimal(str(self.balance))
            
    def clone(self):
        return Moviment(
            data=self.data,
            concepte=self.concepte,
            import_=self.import_,
            balance=self.balance,
            banc=self.banc,
            categoria=self.categoria
        )
    
    @staticmethod
    def clone_list(moviments):
        return [m.clone() for m in moviments]


