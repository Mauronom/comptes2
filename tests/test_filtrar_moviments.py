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
        self.moviments_mostrats = []
        self.total = 0
    def mostrar_moviments(self, movs, total):
        self.moviments_mostrats = movs
        self.total = total
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
    cas_us.execute("super", "", "")

    # --- Assert ---
    assert len(ui.moviments_mostrats) == 1
    assert ui.moviments_mostrats[0].concepte == "Supermercat"
    assert ui.total == 30.0


def test_filtra_moviments_buit_retorna_tots():
    moviments = [
        Moviment(date(2023, 1, 1), "Neteja", 50.0, 100.0, "BancA"),
        Moviment(date(2023, 1, 2), "Supermercat", 30.0, 70.0, "BancA"),
    ]

    repo = FakeRepositori(moviments)
    ui = FakeUI()
    cas_us = FiltrarMoviments(repo, ui)

    cas_us.execute("", "", "")

    assert ui.moviments_mostrats == moviments
    assert ui.total == 80.0


def test_filtra_moviments_per_data_inici():
    # --- Arrange ---
    moviments = [
        Moviment(date(2023, 1, 1), "Neteja", 50.0, 100.0, "BancA"),
        Moviment(date(2023, 1, 15), "Supermercat", 30.0, 70.0, "BancA"),
        Moviment(date(2023, 2, 1), "Lloguer", 500.0, -430.0, "BancB"),
    ]
    
    repo = FakeRepositori(moviments)
    ui = FakeUI()
    cas_us = FiltrarMoviments(repo, ui)

    # --- Act ---
    cas_us.execute("", "2023-01-10", "")

    # --- Assert ---
    assert len(ui.moviments_mostrats) == 2
    assert ui.moviments_mostrats[0].data == date(2023, 1, 15)
    assert ui.moviments_mostrats[1].data == date(2023, 2, 1)
    assert ui.total == 530.0


def test_filtra_moviments_per_data_fi():
    # --- Arrange ---
    moviments = [
        Moviment(date(2023, 1, 1), "Neteja", 50.0, 100.0, "BancA"),
        Moviment(date(2023, 1, 15), "Supermercat", 30.0, 70.0, "BancA"),
        Moviment(date(2023, 2, 1), "Lloguer", 500.0, -430.0, "BancB"),
    ]
    
    repo = FakeRepositori(moviments)
    ui = FakeUI()
    cas_us = FiltrarMoviments(repo, ui)

    # --- Act ---
    cas_us.execute("", "", "2023-01-20")

    # --- Assert ---
    assert len(ui.moviments_mostrats) == 2
    assert ui.moviments_mostrats[0].data == date(2023, 1, 1)
    assert ui.moviments_mostrats[1].data == date(2023, 1, 15)
    assert ui.total == 80.0

def test_filtra_moviments_per_rang_dates():
    # --- Arrange ---
    moviments = [
        Moviment(date(2023, 1, 1), "Neteja", 50.0, 100.0, "BancA"),
        Moviment(date(2023, 1, 15), "Supermercat", 30.0, 70.0, "BancA"),
        Moviment(date(2023, 2, 1), "Lloguer", 500.0, -430.0, "BancB"),
        Moviment(date(2023, 2, 15), "Gasolina", 40.0, -470.0, "BancB"),
    ]
    
    repo = FakeRepositori(moviments)
    ui = FakeUI()
    cas_us = FiltrarMoviments(repo, ui)

    # --- Act ---
    cas_us.execute("", "2023-01-10", "2023-02-05")

    # --- Assert ---
    assert len(ui.moviments_mostrats) == 2
    assert ui.moviments_mostrats[0].data == date(2023, 1, 15)
    assert ui.moviments_mostrats[1].data == date(2023, 2, 1)
    assert ui.total == 530.0

def test_filtra_moviments_concepte_i_dates():
    # --- Arrange ---
    moviments = [
        Moviment(date(2023, 1, 1), "Supermercat", 50.0, 100.0, "BancA"),
        Moviment(date(2023, 1, 15), "Supermercat", 30.0, 70.0, "BancA"),
        Moviment(date(2023, 2, 1), "Lloguer", 500.0, -430.0, "BancB"),
        Moviment(date(2023, 2, 15), "Supermercat", 40.0, -470.0, "BancB"),
    ]
    
    repo = FakeRepositori(moviments)
    ui = FakeUI()
    cas_us = FiltrarMoviments(repo, ui)

    # --- Act ---
    cas_us.execute("super", "2023-01-10", "2023-02-10")

    # --- Assert ---
    assert len(ui.moviments_mostrats) == 1
    assert ui.moviments_mostrats[0].concepte == "Supermercat"
    assert ui.moviments_mostrats[0].data == date(2023, 1, 15)
    assert ui.total == 30.0

def test_filtra_moviments_dates_invalides_ignora_filtre():
    # --- Arrange ---
    moviments = [
        Moviment(date(2023, 1, 1), "Neteja", 50.0, 100.0, "BancA"),
        Moviment(date(2023, 1, 15), "Supermercat", 30.0, 70.0, "BancA"),
    ]
    
    repo = FakeRepositori(moviments)
    ui = FakeUI()
    cas_us = FiltrarMoviments(repo, ui)

    # --- Act --- (dates amb format incorrecte)
    cas_us.execute("", "01/01/2023", "15/01/2023")

    # --- Assert --- (hauria de retornar tots els moviments)
    assert len(ui.moviments_mostrats) == 2
    assert ui.total == 80.0

def test_filtra_moviments_data_inici_posterior_data_fi():
    # --- Arrange ---
    moviments = [
        Moviment(date(2023, 1, 1), "Neteja", 50.0, 100.0, "BancA"),
        Moviment(date(2023, 1, 15), "Supermercat", 30.0, 70.0, "BancA"),
    ]
    
    repo = FakeRepositori(moviments)
    ui = FakeUI()
    cas_us = FiltrarMoviments(repo, ui)

    # --- Act --- (data inici posterior a data fi)
    cas_us.execute("", "2023-01-20", "2023-01-10")

    # --- Assert --- (no hauria de retornar cap moviment)
    assert len(ui.moviments_mostrats) == 0
    assert ui.total == 0.0

def test_filtra_moviments_només_concepte_amb_dates_buides():
    # --- Arrange ---
    moviments = [
        Moviment(date(2023, 1, 1), "Neteja", 50.0, 100.0, "BancA"),
        Moviment(date(2023, 1, 2), "Supermercat", 30.0, 70.0, "BancA"),
    ]
    
    repo = FakeRepositori(moviments)
    ui = FakeUI()
    cas_us = FiltrarMoviments(repo, ui)

    # --- Act ---
    cas_us.execute("super", "", "")

    # --- Assert ---
    assert len(ui.moviments_mostrats) == 1
    assert ui.moviments_mostrats[0].concepte == "Supermercat"
    assert ui.total == 30.0

def test_moviments_filtrats_ordenats_per_data():
    # --- Arrange --- (moviments desordenats intencionalment)
    moviments = [
        Moviment(date(2023, 2, 15), "Gasolina", 40.0, -470.0, "BancB"),
        Moviment(date(2023, 1, 1), "Neteja", 50.0, 100.0, "BancA"),
        Moviment(date(2023, 2, 1), "Lloguer", 500.0, -430.0, "BancB"),
        Moviment(date(2023, 1, 15), "Supermercat", 30.0, 70.0, "BancA"),
    ]
    
    repo = FakeRepositori(moviments)
    ui = FakeUI()
    cas_us = FiltrarMoviments(repo, ui)

    # --- Act ---
    cas_us.execute("", "2023-01-01", "2023-02-28")

    # --- Assert ---
    assert len(ui.moviments_mostrats) == 4
    # Verificar que estan ordenats per data (ascendent)
    dates = [m.data for m in ui.moviments_mostrats]
    assert dates == [date(2023, 1, 1), date(2023, 1, 15), date(2023, 2, 1), date(2023, 2, 15)]
    assert ui.total == 620.0

def test_moviments_filtrats_per_concepte_ordenats_per_data():
    # --- Arrange --- (moviments amb mateix concepte però dates desordenades)
    moviments = [
        Moviment(date(2023, 2, 15), "Supermercat", 25.0, 50.0, "BancA"),
        Moviment(date(2023, 1, 5), "Supermercat", 30.0, 70.0, "BancA"),
        Moviment(date(2023, 1, 20), "Lloguer", 500.0, -430.0, "BancB"),
        Moviment(date(2023, 1, 15), "Supermercat", 40.0, 30.0, "BancB"),
    ]
    
    repo = FakeRepositori(moviments)
    ui = FakeUI()
    cas_us = FiltrarMoviments(repo, ui)

    # --- Act ---
    cas_us.execute("super", "", "")

    # --- Assert ---
    assert len(ui.moviments_mostrats) == 3
    # Verificar que els moviments del supermercat estan ordenats per data
    dates = [m.data for m in ui.moviments_mostrats]
    assert dates == [date(2023, 1, 5), date(2023, 1, 15), date(2023, 2, 15)]
    # Verificar que tots són del supermercat
    for moviment in ui.moviments_mostrats:
        assert "supermercat" in moviment.concepte.lower()
    assert ui.total == 95.0