import pytest
from datetime import date
from domain import Moviment
from app import FiltrarMoviments

class FakeRepositori:
    def __init__(self, movs):
        self.moviments = movs
    def obtenir_tots(self):
        return self.moviments

class FakeUI:
    def __init__(self):
        self.moviments_mostrats = None
    def mostrar_moviments(self, movs):
        self.moviments_mostrats = movs
    def print(self, info):
        print(str(info))


def test_filtra_moviments_per_concepte():
    # --- Arrange ---
    moviments = [
        Moviment(date(2023, 1, 1), "Neteja", 50.0, 100.0, "BancA"),
        Moviment(date(2023, 1, 2), "Supermercat", 30.0, 70.0, "BancA"),
        Moviment(date(2023, 1, 3), "Lloguer", 500.0, -430.0, "BancB"),
    ]
    
    repo = FakeRepositori(moviments)
    ui = FakeUI()
    cas_us = FiltrarMoviments(repo, ui)

    # --- Act ---
    cas_us.execute("super")

    # --- Assert ---
    assert len(ui.moviments_mostrats) == 1
    assert ui.moviments_mostrats[0].concepte == "Supermercat"


def test_filtra_moviments_buit_retornat_tots():
    moviments = [
        Moviment(date(2023, 1, 1), "Neteja", 50.0, 100.0, "BancA"),
        Moviment(date(2023, 1, 2), "Supermercat", 30.0, 70.0, "BancA"),
    ]

    repo = FakeRepositori(moviments)
    ui = FakeUI()
    cas_us = FiltrarMoviments(repo, ui)

    cas_us.execute("")

    assert ui.moviments_mostrats == moviments
