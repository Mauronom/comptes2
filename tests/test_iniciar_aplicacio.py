import unittest
from datetime import date
from domain import Moviment
from app import IniciarAplicacio
from infra import MemoryCategoriesRepo


class FakeUI:
    def __init__(self):
        self.moviments_mostrats = []
        self.total = 0

    def mostrar_moviments(self, moviments, total, diari, mensual):
        self.moviments_mostrats = moviments
        self.total = total
        self.diari = diari
        self.mensual = mensual

class FakeRepositori:
    def __init__(self,):
        self.moviments = [
            Moviment(date(2025, 1, 1), "Sou",2000.0, 5000.0, "Banc A"),
            Moviment(date(2025, 1, 2), "Compra supermercat", -50.0, 4950.0, "Banc A"),
            Moviment(date(2025, 1, 3), "PLAN AHORRO 5 SIALP", -100.0, 4850.0, "Banc B"),
            Moviment(date(2025, 1, 5), "CI PIAS", -100.0, 4750.0, "Banc B"),
        ]

    def obtenir_tots(self):
        return Moviment.clone_list(self.moviments)

    def enriquir(self,movs):
        self.moviments.extend(movs)

    def save(self,movs):
        self.moviments = Moviment.clone_list(movs)

class TestIniciarAplicacio(unittest.TestCase):
    def test_execute_mostra_moviments(self):
        repo = FakeRepositori()
        repo_cats = MemoryCategoriesRepo({
            "ingrés": ["Sou"],
            "alimentació": ["Compra supermercat"],
            "estalvi": ["PLAN AHORRO 5 SIALP", "CI PIAS","SIALP PIES"],
        })
        ui = FakeUI()
        cas_ús = IniciarAplicacio(repo, ui, repo_cats)

        cas_ús.execute()
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
        self.assertEqual(ui.moviments_mostrats[0].categoria, "ingrés")
        self.assertEqual(ui.moviments_mostrats[1].categoria, "alimentació")
        self.assertEqual(ui.moviments_mostrats[2].categoria, "estalvi")
        self.assertEqual(ui.moviments_mostrats[3].categoria, "estalvi")
        self.assertEqual(ui.moviments_mostrats[4].categoria, "estalvi")
        self.assertEqual(ui.moviments_mostrats[5].categoria, "estalvi")
        self.assertEqual(ui.total, 1950.0)
        self.assertEqual(ui.diari, 1950.0/5)
        self.assertEqual(ui.mensual, 30*1950.0/5)



if __name__ == "__main__":
    unittest.main()
