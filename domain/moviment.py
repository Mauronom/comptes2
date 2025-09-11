from dataclasses import dataclass
from datetime import date

@dataclass
class Moviment:
    data: date
    concepte: str
    import_: float
    balance: float
    banc: str

    def clone(self):
        return Moviment(
            data=self.data,
            concepte=self.concepte,
            import_=self.import_,
            balance=self.balance,
            banc=self.banc
        )
    
    @staticmethod
    def clone_list(moviments):
        return [m.clone() for m in moviments]


