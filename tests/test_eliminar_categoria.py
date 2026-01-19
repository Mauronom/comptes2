import pytest
from app import EliminarCategoria  # This will be created later


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

    def delete(self, name):
        if name in self.categories:
            del self.categories[name]
            return True
        return False


def test_eliminar_categoria_removes_existing_category():
    """Test that EliminarCategoria removes an existing category from the repository"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    cas_us = EliminarCategoria(fake_repo)

    # --- Act ---
    result = cas_us.execute("transport")

    # --- Assert ---
    assert result is True  # Indicating success
    assert "transport" not in fake_repo.categories
    assert len(fake_repo.categories) == 2  # Only 2 categories should remain
    # Verify other categories remain unchanged
    assert "alimentació" in fake_repo.categories
    assert "habitatge" in fake_repo.categories


def test_eliminar_categoria_nonexistent_category():
    """Test that EliminarCategoria handles non-existent category appropriately"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    cas_us = EliminarCategoria(fake_repo)

    # --- Act ---
    result = cas_us.execute("categoria_inexistent")

    # --- Assert ---
    assert result is False  # Indicating failure/couldn't find category
    assert len(fake_repo.categories) == 3  # No categories should be removed


def test_eliminar_categoria_last_category():
    """Test that EliminarCategoria works when removing the last category"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo({"única": ["paraula1", "paraula2"]})
    cas_us = EliminarCategoria(fake_repo)

    # --- Act ---
    result = cas_us.execute("única")

    # --- Assert ---
    assert result is True  # Indicating success
    assert len(fake_repo.categories) == 0  # No categories should remain


def test_eliminar_categoria_case_sensitivity():
    """Test that EliminarCategoria handles case sensitivity correctly"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo({"Alimentació": ["supermercat", "fruits"]})
    cas_us = EliminarCategoria(fake_repo)

    # --- Act ---
    result = cas_us.execute("alimentació")  # Different case

    # --- Assert ---
    assert result is False  # Should not find the category due to case sensitivity
    assert len(fake_repo.categories) == 1  # Category should still exist