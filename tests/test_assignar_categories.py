import unittest
from datetime import date
from domain import Moviment
from app import AssignarCategories
from infra import MemoryCategoriesRepo


class FakeRepositoriMoviments:
    """Fake repository for testing"""

    def __init__(self, moviments=None):
        if moviments is None:
            moviments = []
        self.moviments = Moviment.clone_list(moviments)

    def obtenir_tots(self):
        return Moviment.clone_list(self.moviments)

    def save(self, moviments):
        self.moviments = Moviment.clone_list(moviments)


class FakeUI:
    """Fake UI for testing"""

    def __init__(self):
        self.moviments_mostrats = []
        self.total = 0
        self.diari = 0
        self.mensual = 0

    def mostrar_moviments(self, moviments, total, diari, mensual):
        self.moviments_mostrats = moviments
        self.total = total
        self.diari = diari
        self.mensual = mensual


class TestAssignarCategories(unittest.TestCase):

    def test_assignar_categories_assigns_matching_categories(self):
        """Test that AssignarCategories assigns categories based on keyword matching"""
        # --- Arrange ---
        moviments = [
            Moviment(date(2025, 1, 1), "Compra supermercat", 50.0, 1000.0, "Banc A"),
            Moviment(date(2025, 1, 2), "Taxi centre ciutat", 15.0, 985.0, "Banc A"),
            Moviment(date(2025, 1, 3), "Factura electricitat", 80.0, 905.0, "Banc B")
        ]
        
        repositori_moviments = FakeRepositoriMoviments(moviments)
        repositori_categories = MemoryCategoriesRepo({
            "alimentació": ["supermercat", "fruits", "verdura"],
            "transport": ["taxi", "autobús", "tren"],
            "habitatge": ["electricitat", "aigua", "gas"]
        })
        
        ui = FakeUI()
        cas_us = AssignarCategories(repositori_moviments, ui, repositori_categories)

        # --- Act ---
        cas_us.execute()

        # --- Assert ---
        # Retrieve the saved movements to check categories
        saved_moviments = repositori_moviments.obtenir_tots()
        
        # Check that categories were assigned correctly
        self.assertEqual(saved_moviments[0].categoria, "alimentació")  # "supermercat" matches "alimentació"
        self.assertEqual(saved_moviments[1].categoria, "transport")    # "taxi" matches "transport"
        self.assertEqual(saved_moviments[2].categoria, "habitatge")   # "electricitat" matches "habitatge"

    def test_assignar_categories_assigns_default_category_when_no_match(self):
        """Test that AssignarCategories assigns 'altres' category when no keywords match"""
        # --- Arrange ---
        moviments = [
            Moviment(date(2025, 1, 1), "Regal nadalenc", 50.0, 1000.0, "Banc A"),
            Moviment(date(2025, 1, 2), "Sortida cinema", 12.0, 988.0, "Banc A")
        ]
        
        repositori_moviments = FakeRepositoriMoviments(moviments)
        repositori_categories = MemoryCategoriesRepo({
            "alimentació": ["supermercat", "fruits", "verdura"],
            "transport": ["taxi", "autobús", "tren"]
        })
        
        ui = FakeUI()
        cas_us = AssignarCategories(repositori_moviments, ui, repositori_categories)

        # --- Act ---
        cas_us.execute()

        # --- Assert ---
        saved_moviments = repositori_moviments.obtenir_tots()
        
        # Check that default 'altres' category was assigned
        self.assertEqual(saved_moviments[0].categoria, "altres")  # No match
        self.assertEqual(saved_moviments[1].categoria, "altres")  # No match

    def test_assignar_categories_updates_ui_with_new_categories(self):
        """Test that AssignarCategories updates the UI with movements having new categories"""
        # --- Arrange ---
        moviments = [
            Moviment(date(2025, 1, 1), "Compra supermercat", 50.0, 1000.0, "Banc A", "altres"),
            Moviment(date(2025, 1, 2), "Taxi centre ciutat", 15.0, 985.0, "Banc A", "altres")
        ]
        
        repositori_moviments = FakeRepositoriMoviments(moviments)
        repositori_categories = MemoryCategoriesRepo({
            "alimentació": ["supermercat", "fruits"],
            "transport": ["taxi", "autobús"]
        })
        
        ui = FakeUI()
        cas_us = AssignarCategories(repositori_moviments, ui, repositori_categories)

        # --- Act ---
        cas_us.execute()

        # --- Assert ---
        # Check that UI was updated with movements having correct categories
        self.assertEqual(len(ui.moviments_mostrats), 2)
        self.assertEqual(ui.moviments_mostrats[0].categoria, "alimentació")  # "supermercat" matches
        self.assertEqual(ui.moviments_mostrats[1].categoria, "transport")    # "taxi" matches

    def test_assignar_categories_preserves_existing_movements_properties(self):
        """Test that AssignarCategories preserves all movement properties except category"""
        # --- Arrange ---
        moviments = [
            Moviment(date(2025, 1, 1), "Compra supermercat", 50.0, 1000.0, "Banc A", "original")
        ]
        
        repositori_moviments = FakeRepositoriMoviments(moviments)
        repositori_categories = MemoryCategoriesRepo({
            "alimentació": ["supermercat"]
        })
        
        ui = FakeUI()
        cas_us = AssignarCategories(repositori_moviments, ui, repositori_categories)

        # --- Act ---
        cas_us.execute()

        # --- Assert ---
        saved_moviments = repositori_moviments.obtenir_tots()
        original_movement = moviments[0]
        updated_movement = saved_moviments[0]
        
        # Check that all properties except category are preserved
        self.assertEqual(updated_movement.data, original_movement.data)
        self.assertEqual(updated_movement.concepte, original_movement.concepte)
        self.assertEqual(updated_movement.import_, original_movement.import_)
        self.assertEqual(updated_movement.balance, original_movement.balance)
        self.assertEqual(updated_movement.banc, original_movement.banc)
        self.assertEqual(updated_movement.categoria, "alimentació")  # Category should be updated

    def test_assignar_categories_handles_empty_categories_repo(self):
        """Test that AssignarCategories handles empty categories repository"""
        # --- Arrange ---
        moviments = [
            Moviment(date(2025, 1, 1), "Compra supermercat", 50.0, 1000.0, "Banc A")
        ]
        
        repositori_moviments = FakeRepositoriMoviments(moviments)
        repositori_categories = MemoryCategoriesRepo({})  # Empty categories
        
        ui = FakeUI()
        cas_us = AssignarCategories(repositori_moviments, ui, repositori_categories)

        # --- Act ---
        cas_us.execute()

        # --- Assert ---
        saved_moviments = repositori_moviments.obtenir_tots()
        
        # All movements should have 'altres' category since no categories exist
        self.assertEqual(saved_moviments[0].categoria, "altres")

    def test_assignar_categories_case_insensitive_matching(self):
        """Test that AssignarCategories performs case-insensitive keyword matching"""
        # --- Arrange ---
        moviments = [
            Moviment(date(2025, 1, 1), "COMPRA SUPERMERCAT", 50.0, 1000.0, "Banc A"),
            Moviment(date(2025, 1, 2), "taxi centre ciutat", 15.0, 985.0, "Banc A")
        ]
        
        repositori_moviments = FakeRepositoriMoviments(moviments)
        repositori_categories = MemoryCategoriesRepo({
            "alimentació": ["supermercat", "fruits"],
            "transport": ["TAXI", "autobús"]
        })
        
        ui = FakeUI()
        cas_us = AssignarCategories(repositori_moviments, ui, repositori_categories)

        # --- Act ---
        cas_us.execute()

        # --- Assert ---
        saved_moviments = repositori_moviments.obtenir_tots()
        
        # Check that case-insensitive matching worked
        self.assertEqual(saved_moviments[0].categoria, "alimentació")  # "COMPRA SUPERMERCAT" matches "supermercat"
        self.assertEqual(saved_moviments[1].categoria, "transport")    # "taxi centre ciutat" matches "TAXI"


if __name__ == '__main__':
    unittest.main()