import unittest
from datetime import date
from domain import Moviment, ReglaMovimentFictici, ConfigMovimentsFicticisRepo
from app import IniciarAplicacio
from infra import MemoryCategoriesRepo, MemoryConfigMovimentsFicticisRepo


class FakeUI:
    def __init__(self):
        self.moviments_mostrats = []
        self.total = 0
        self.directori_demanat = False
        self.directori_retornat = "/fake/path"

    def mostrar_moviments(self, moviments, total, diari, mensual):
        self.moviments_mostrats = moviments
        self.total = total
        self.diari = diari
        self.mensual = mensual

    def demanar_directori(self):
        self.directori_demanat = True
        return self.directori_retornat

class FakeRepositori:
    def __init__(self):
        self.moviments = [
            Moviment(date(2025, 1, 1), "Sou",2000.0, 5000.0, "Banc A"),
            Moviment(date(2025, 1, 2), "Compra supermercat", -50.0, 4950.0, "Banc A"),
            Moviment(date(2025, 1, 3), "PLAN AHORRO 5 SIALP", -100.0, 4850.0, "Banc B"),
            Moviment(date(2025, 1, 5), "CI PIAS", -100.0, 4750.0, "Banc B"),
        ]
        self.directori_rebut = None

    def set_directori(self, directori):
        self.directori_rebut = directori

    def obtenir_tots(self):
        return Moviment.clone_list(self.moviments)

    def enriquir(self, movs):
        self.moviments.extend(movs)

    def save(self, movs):
        self.moviments = Moviment.clone_list(movs)

class TestIniciarAplicacio(unittest.TestCase):
    def test_execute_demana_directori_i_passa_al_repositori(self):
        repo = FakeRepositori()
        repo_cats = MemoryCategoriesRepo({
            "ingrés": ["sou"],
            "alimentació": ["Compra supermercat"],
            "estalvi": ["PLAN AHORRO 5 SIALP", "CI PIAS","SIALP PIES"],
        })
        
        # Configurar repositori de moviments ficticis amb regla i moviment inicial
        regla_sialp = ReglaMovimentFictici(
            patrons=["PLAN AHORRO 5 SIALP", "CI PIAS"],
            concepte_desti="SIALP PIES",
            banc_desti="SIALP_PIAS",
            invertir_import=True
        )
        moviment_inicial = Moviment(
            data=date(2024, 8, 1),
            concepte="SIALP PIES",
            import_=0,
            balance=17000,
            banc="SIALP_PIAS"
        )
        repo_config = MemoryConfigMovimentsFicticisRepo([regla_sialp], [moviment_inicial])
        
        ui = FakeUI()
        cas_ús = IniciarAplicacio(repo, ui, repo_cats, repo_config)

        cas_ús.execute()

        # ✅ comprovar que primer s'ha demanat el directori
        self.assertTrue(ui.directori_demanat)

        # ✅ comprovar que el repositori ha rebut el directori correcte
        self.assertEqual(repo.directori_rebut, ui.directori_retornat)

        # ✅ comprovar que es mostren els moviments (4 originals + 1 inicial + 2 ficticis)
        self.assertIsNotNone(ui.moviments_mostrats)
        self.assertEqual(len(repo.moviments), 7)  # Actualitzat per incloure el moviment inicial
        self.assertEqual(len(ui.moviments_mostrats), 7)
        
        # Trobar el moviment inicial (hauria de ser el primer per data)
        moviment_inicial_trobat = next((m for m in ui.moviments_mostrats if m.data == date(2024, 8, 1)), None)
        self.assertIsNotNone(moviment_inicial_trobat)
        self.assertEqual(moviment_inicial_trobat.concepte, "SIALP PIES")
        self.assertEqual(moviment_inicial_trobat.balance, 17000)
        self.assertEqual(moviment_inicial_trobat.banc, "SIALP_PIAS")
        
        # Verificar que hi ha moviments amb concepte "SIALP PIES" dels ficticis
        moviments_sialp_ficticis = [m for m in ui.moviments_mostrats if m.concepte == "SIALP PIES" and m.data != date(2024, 8, 1)]
        self.assertEqual(len(moviments_sialp_ficticis), 2)  # Els dos moviments ficticis

    def test_sense_repositori_config_no_afegeix_moviments_ficticis(self):
        """Test que verifica que sense repositori de config no s'afegeixen moviments ficticis"""
        repo = FakeRepositori()
        repo_cats = MemoryCategoriesRepo({})
        ui = FakeUI()
        cas_ús = IniciarAplicacio(repo, ui, repo_cats)  # Sense repositori config

        cas_ús.execute()

        # Només hauria de tenir els 4 moviments originals
        self.assertEqual(len(ui.moviments_mostrats), 4)

    def test_amb_repositori_config_buit_no_afegeix_moviments_ficticis(self):
        """Test que verifica que amb repositori de config buit no s'afegeixen moviments ficticis"""
        repo = FakeRepositori()
        repo_cats = MemoryCategoriesRepo({})
        repo_config = MemoryConfigMovimentsFicticisRepo([], [])  # Repositori buit
        ui = FakeUI()
        cas_ús = IniciarAplicacio(repo, ui, repo_cats, repo_config)

        cas_ús.execute()

        # Només hauria de tenir els 4 moviments originals
        self.assertEqual(len(ui.moviments_mostrats), 4)

    def test_moviments_inicials_nomes(self):
        """Test que verifica que els moviments inicials s'afegeixen correctament sense regles"""
        repo = FakeRepositori()
        repo_cats = MemoryCategoriesRepo({})
        
        moviment_inicial = Moviment(
            data=date(2024, 7, 1),
            concepte="Balance inicial",
            import_=0,
            balance=1000,
            banc="TEST_BANC"
        )
        repo_config = MemoryConfigMovimentsFicticisRepo([], [moviment_inicial])
        
        ui = FakeUI()
        cas_ús = IniciarAplicacio(repo, ui, repo_cats, repo_config)

        cas_ús.execute()

        # 4 moviments originals + 1 inicial
        self.assertEqual(len(ui.moviments_mostrats), 5)
        
        # Verificar que el moviment inicial està present
        moviment_trobat = next((m for m in ui.moviments_mostrats if m.concepte == "Balance inicial"), None)
        self.assertIsNotNone(moviment_trobat)
        self.assertEqual(moviment_trobat.banc, "TEST_BANC")



if __name__ == "__main__":
    unittest.main()