import pytest
from app import EditarCategoria  # This will be created later


class FakeCategoriesRepo:
    """Fake repository for testing"""
    
    def __init__(self, categories=None):
        if categories is None:
            categories = {
                "alimentació": ["supermercat", "fruits", "verdures"],
                "transport": ["gasolina", "autobús", "tren"],
                "habitatge": ["lloguer", "aigua", "electricitat"]
            }
        self.categories = categories

    def get_all(self):
        return self.categories

    def find_by_name(self, name):
        return self.categories.get(name)

    def save(self, name, texts):
        self.categories[name] = texts


def test_editar_categoria_updates_existing_category():
    """Test that EditarCategoria updates an existing category in the repository"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    cas_us = EditarCategoria(fake_repo)

    # --- Act ---
    cas_us.execute("alimentació", ["supermercat", "carn", "peix"])

    # --- Assert ---
    assert "alimentació" in fake_repo.categories
    assert fake_repo.categories["alimentació"] == ["supermercat", "carn", "peix"]
    # Verify other categories remain unchanged
    assert "transport" in fake_repo.categories
    assert fake_repo.categories["transport"] == ["gasolina", "autobús", "tren"]


def test_editar_categoria_with_nonexistent_category():
    """Test that EditarCategoria creates a new category if it doesn't exist"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    cas_us = EditarCategoria(fake_repo)

    # --- Act ---
    cas_us.execute("ocidi", ["cinema", "teatre", "restaurants"])

    # --- Assert ---
    assert "ocidi" in fake_repo.categories
    assert fake_repo.categories["ocidi"] == ["cinema", "teatre", "restaurants"]
    # Verify other categories remain unchanged
    assert "alimentació" in fake_repo.categories


def test_editar_categoria_with_empty_keywords():
    """Test that EditarCategoria can handle empty keywords list"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    cas_us = EditarCategoria(fake_repo)

    # --- Act ---
    cas_us.execute("habitatge", [])

    # --- Assert ---
    assert "habitatge" in fake_repo.categories
    assert fake_repo.categories["habitatge"] == []


def test_editar_categoria_with_special_characters():
    """Test that EditarCategoria handles special characters correctly"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    cas_us = EditarCategoria(fake_repo)

    # --- Act ---
    cas_us.execute("ocasió especial", ["café", "naïf", "fiançailles"])

    # --- Assert ---
    assert "ocasió especial" in fake_repo.categories
    assert fake_repo.categories["ocasió especial"] == ["café", "naïf", "fiançailles"]