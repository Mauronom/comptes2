import pytest
from app import MostrarCategories  # This will be created later


class FakeCategoriesRepo:
    """Fake repository for testing"""
    
    def __init__(self, categories=None):
        if categories is None:
            categories = {
                "alimentació": ["supermercat", "fruits", "verdures"],
                "transport": ["gasolina", "autobús", "tren"],
                "habitatge": ["lloguer", "aigua", "electricitat"],
                "ocidi": ["restaurants", "cinema", "viatges"]
            }
        self.categories = categories

    def get_all(self):
        return self.categories

    def find_by_name(self, name):
        return self.categories.get(name)

    def save(self, name, texts):
        self.categories[name] = texts


class FakeUI:
    """Fake UI for testing"""
    
    def __init__(self):
        self.categories_shown = None
    
    def mostrar_categories(self, categories):
        """Method that UI will call to show categories"""
        self.categories_shown = categories


def test_mostrar_categories_returns_all_categories():
    """Test that MostrarCategories returns all categories from the repository"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    fake_ui = FakeUI()
    cas_us = MostrarCategories(fake_repo, fake_ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert fake_ui.categories_shown is not None
    assert len(fake_ui.categories_shown) == 4  # We have 4 categories in our fake repo
    assert "alimentació" in fake_ui.categories_shown
    assert "transport" in fake_ui.categories_shown
    assert "habitatge" in fake_ui.categories_shown
    assert "ocidi" in fake_ui.categories_shown
    
    # Check that each category has associated keywords
    assert fake_ui.categories_shown["alimentació"] == ["supermercat", "fruits", "verdures"]
    assert fake_ui.categories_shown["transport"] == ["gasolina", "autobús", "tren"]
    assert fake_ui.categories_shown["habitatge"] == ["lloguer", "aigua", "electricitat"]
    assert fake_ui.categories_shown["ocidi"] == ["restaurants", "cinema", "viatges"]


def test_mostrar_categories_empty_repo():
    """Test that MostrarCategories handles empty repository correctly"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo(categories={})
    fake_ui = FakeUI()
    cas_us = MostrarCategories(fake_repo, fake_ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert fake_ui.categories_shown is not None
    assert len(fake_ui.categories_shown) == 0


def test_mostrar_categories_single_category():
    """Test that MostrarCategories handles repository with single category"""
    # --- Arrange ---
    single_category = {"salari": ["nomina", "paga"]}
    fake_repo = FakeCategoriesRepo(categories=single_category)
    fake_ui = FakeUI()
    cas_us = MostrarCategories(fake_repo, fake_ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert fake_ui.categories_shown is not None
    assert len(fake_ui.categories_shown) == 1
    assert "salari" in fake_ui.categories_shown
    assert fake_ui.categories_shown["salari"] == ["nomina", "paga"]