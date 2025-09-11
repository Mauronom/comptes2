import pytest
from unittest.mock import Mock
from datetime import date, datetime
from domain import Moviment
from app import MostrarGraficaBalance

class FakeRepositori:
    def obtenir_tots(self):
        return [
            Moviment(data=date(2023, 1, 1), concepte="Sou", import_=1000, balance=1000, banc="TestBank"),
            Moviment(data=date(2023, 1, 1), concepte="Compra matí", import_=-100, balance=900, banc="TestBank"),
            Moviment(data=date(2023, 1, 1), concepte="Alt banc", import_=200, balance=200, banc="OtherBank"),
            Moviment(data=date(2023, 1, 2), concepte="Lloguer", import_=-500, balance=350, banc="TestBank"),
        ]

def test_mostrar_grafica_converteix_moviments_a_punts_amb_banc():
    repositori = FakeRepositori()
    ui = Mock()

    usecase = MostrarGraficaBalance(ui)
    usecase.execute(repositori.obtenir_tots())

    assert ui.mostrar_grafica.call_count == 1
    args, _ = ui.mostrar_grafica.call_args_list[0]
    dades = args[0]

    # Els punts han de tenir datetime + balance + banc
    esperats = [
        (datetime(2023, 1, 1, 0, 0, 0), 200, "OtherBank", "Alt banc", 200),
        (datetime(2023, 1, 1, 0, 0, 0), 1000, "TestBank", "Sou", 1000),
        (datetime(2023, 1, 1, 0, 0, 0), 1200, "Total","Total", 1200),
        (datetime(2023, 1, 1, 1, 0, 0), 900, "TestBank", "Compra matí", -100),
        (datetime(2023, 1, 1, 1, 0, 0), 1100, "Total" ,"Total", -100),
        (datetime(2023, 1, 2, 0, 0, 0), 350, "TestBank", "Lloguer", -500),
        (datetime(2023, 1, 2, 0, 0, 0), 550, "Total", "Total", -500),
    ]
    assert dades["punts"] == esperats

    # Els eixos han de ser coherents
    assert dades["etiqueta_x"] == "Data/Hora"
    assert dades["etiqueta_y"] == "Balanç"

    