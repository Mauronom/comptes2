from dataclasses import dataclass
from datetime import date

@dataclass
class Moviment:
    data: date
    concepte: str
    import_: float
    balance: float
    banc: str


