import pytest
from unittest.mock import Mock
from datetime import date, datetime
from domain import Moviment
from app import MostrarGraficaCategories

class FakeRepositori:
    def obtenir_tots(self):
        return [
            Moviment(data=date(2023, 1, 1), concepte="Sou", import_=1000, balance=1000, banc="TestBank",categoria="nomina"),
            Moviment(data=date(2023, 1, 1), concepte="Compra matí", import_=-100, balance=900, banc="TestBank",categoria="alimentació"),
            Moviment(data=date(2023, 1, 1), concepte="Alt banc", import_=200, balance=200, banc="OtherBank",categoria="habitatge"),
            Moviment(data=date(2023, 1, 2), concepte="Lloguer", import_=-500, balance=350, banc="TestBank", categoria="habitatge"),
        ]

def test_mostrar_grafica_converteix_moviments_despeses_per_categoria():
    repositori = FakeRepositori()
    ui = Mock()

    usecase = MostrarGraficaCategories(ui)
    usecase.execute(repositori.obtenir_tots())

    assert ui.mostrar_grafica_categories.call_count == 1
    args, _ = ui.mostrar_grafica_categories.call_args_list[0]
    assert args[0] == {'alimentació': -100.0, 'habitatge': -300.0}

    