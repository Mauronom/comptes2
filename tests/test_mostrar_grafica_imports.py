import pytest
from unittest.mock import Mock
from datetime import date, datetime
from domain import Moviment
from app import MostrarGraficaImports

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

    usecase = MostrarGraficaImports(ui)
    usecase.execute(repositori.obtenir_tots())

    assert ui.mostrar_grafica.call_count == 1
    args, _ = ui.mostrar_grafica.call_args_list[0]
    dades = args[0]

    # Els punts han de tenir datetime + balance + banc
    esperats = [
        (datetime(2023, 1, 1, 0, 0, 0), 200, "OtherBank"),
        (datetime(2023, 1, 1, 0, 0, 0), 1000, "TestBank"),
        (datetime(2023, 1, 1, 0, 0, 0), 1200, "Total"),
        (datetime(2023, 1, 1, 1, 0, 0), 900, "TestBank"),
        (datetime(2023, 1, 1, 1, 0, 0), 1100, "Total"),
        (datetime(2023, 1, 2, 0, 0, 0), 400, "TestBank"),
        (datetime(2023, 1, 2, 0, 0, 0), 600, "Total"),
    ]
    assert dades["punts"] == esperats

    # Els eixos han de ser coherents
    assert dades["etiqueta_x"] == "Data/Hora"
    assert dades["etiqueta_y"] == "Import Acumulat"

    