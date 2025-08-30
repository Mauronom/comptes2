import unittest
from datetime import date
from domain import Moviment
from app import IniciarAplicacio

class FakeUI:
    def __init__(self):
        self.moviments_mostrats = None

    def mostrar_moviments(self, moviments):
        self.moviments_mostrats = moviments

class FakeRepositori:
    def __init__(self,):
        self.moviments = [
            Moviment(date(2025, 1, 1), "Sou",2000.0, 5000.0, "Banc A"),
            Moviment(date(2025, 1, 2), "Compra supermercat", -50.0, 4950.0, "Banc A"),
            Moviment(date(2025, 1, 3), "PLAN UNI SEGUR", -100.0, 4850.0, "Banc B"),
            Moviment(date(2025, 1, 4), "PLAN UNI SEGUR", -100.0, 4750.0, "Banc B"),
        ]

    def obtenir_tots(self):
        return self.moviments.copy()

    def enriquir(self,movs):
        self.moviments.extend(movs)


class TestIniciarAplicacio(unittest.TestCase):
    def test_execute_mostra_moviments(self):
        repo = FakeRepositori()
        ui = FakeUI()
        cas_ús = IniciarAplicacio(repo, ui)

        cas_ús.execute()
        for m in ui.moviments_mostrats:
            print(m)
        self.assertIsNotNone(ui.moviments_mostrats)
        self.assertEqual(len(repo.moviments), 6)
        self.assertEqual(len(ui.moviments_mostrats), 6)
        self.assertEqual(ui.moviments_mostrats[0].concepte, "Sou")
        self.assertEqual(ui.moviments_mostrats[1].import_, -50.0)
        self.assertEqual(ui.moviments_mostrats[2].import_, -100.0)
        self.assertEqual(ui.moviments_mostrats[3].import_, 100.0)
        self.assertEqual(ui.moviments_mostrats[3].banc, "SIALP_PIAS")
        self.assertEqual(ui.moviments_mostrats[3].balance, 100.0)
        self.assertEqual(ui.moviments_mostrats[4].import_, -100.0)
        self.assertEqual(ui.moviments_mostrats[5].import_, 100.0)
        self.assertEqual(ui.moviments_mostrats[5].banc, "SIALP_PIAS")
        self.assertEqual(ui.moviments_mostrats[5].balance, 200.0)

if __name__ == "__main__":
    unittest.main()
