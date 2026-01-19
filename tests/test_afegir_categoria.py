import pytest
from app import AfegirCategoria  # This will be created later


class FakeCategoriesRepo:
    """Fake repository for testing"""
    
    def __init__(self, categories=None):
        if categories is None:
            categories = {}
        self.categories = categories

    def get_all(self):
        return self.categories

    def find_by_name(self, name):
        return self.categories.get(name)

    def save(self, name, texts):
        self.categories[name] = texts


def test_afegir_categoria_creates_new_category():
    """Test that AfegirCategoria creates a new category in the repository"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    cas_us = AfegirCategoria(fake_repo)

    # --- Act ---
    cas_us.execute("alimentació", ["supermercat", "fruits", "verdures"])

    # --- Assert ---
    assert "alimentació" in fake_repo.categories
    assert fake_repo.categories["alimentació"] == ["supermercat", "fruits", "verdures"]


def test_afegir_categoria_overwrites_existing_category():
    """Test that AfegirCategoria overwrites an existing category"""
    # --- Arrange ---
    initial_categories = {"transport": ["gasolina", "autobús"]}
    fake_repo = FakeCategoriesRepo(initial_categories)
    cas_us = AfegirCategoria(fake_repo)

    # --- Act ---
    cas_us.execute("transport", ["taxi", "metro"])

    # --- Assert ---
    assert "transport" in fake_repo.categories
    assert fake_repo.categories["transport"] == ["taxi", "metro"]


def test_afegir_categoria_with_empty_keywords():
    """Test that AfegirCategoria can handle empty keywords list"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    cas_us = AfegirCategoria(fake_repo)

    # --- Act ---
    cas_us.execute("categoria_buida", [])

    # --- Assert ---
    assert "categoria_buida" in fake_repo.categories
    assert fake_repo.categories["categoria_buida"] == []


def test_afegir_categoria_with_special_characters():
    """Test that AfegirCategoria handles special characters correctly"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    cas_us = AfegirCategoria(fake_repo)

    # --- Act ---
    cas_us.execute("ocasió especial", ["café", "naïf", "fiançailles"])

    # --- Assert ---
    assert "ocasió especial" in fake_repo.categories
    assert fake_repo.categories["ocasió especial"] == ["café", "naïf", "fiançailles"]