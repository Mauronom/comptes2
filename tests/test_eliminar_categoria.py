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


class DirectUIForDelete:
    """UI implementation that returns predefined values for testing delete operations"""

    def __init__(self, nom_categoria, confirmacio=True):
        self.nom_categoria = nom_categoria
        self.confirmacio = confirmacio
        self.popup_messages = []  # Track popup messages for testing

    def input_popup(self, text, title, default_text=None):
        """Return the predefined category name"""
        return self.nom_categoria

    def mostrar_popup(self, titol, text):
        """Track popup messages for testing purposes"""
        self.popup_messages.append((titol, text))

    def confirmar_accio(self, missatge):
        """Return predefined confirmation value for testing"""
        return self.confirmacio


def test_eliminar_categoria_removes_existing_category():
    """Test that EliminarCategoria removes an existing category from the repository"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    ui = DirectUIForDelete("transport", confirmacio=True)
    cas_us = EliminarCategoria(fake_repo, ui)

    # --- Act ---
    result = cas_us.execute()

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
    ui = DirectUIForDelete("categoria_inexistent", confirmacio=True)
    cas_us = EliminarCategoria(fake_repo, ui)

    # --- Act ---
    result = cas_us.execute()

    # --- Assert ---
    assert result is False  # Indicating failure/couldn't find category
    assert len(fake_repo.categories) == 3  # No categories should be removed


def test_eliminar_categoria_last_category():
    """Test that EliminarCategoria works when removing the last category"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo({"única": ["paraula1", "paraula2"]})
    ui = DirectUIForDelete("única", confirmacio=True)
    cas_us = EliminarCategoria(fake_repo, ui)

    # --- Act ---
    result = cas_us.execute()

    # --- Assert ---
    assert result is True  # Indicating success
    assert len(fake_repo.categories) == 0  # No categories should remain


def test_eliminar_categoria_case_sensitivity():
    """Test that EliminarCategoria handles case sensitivity correctly"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo({"Alimentació": ["supermercat", "fruits"]})
    ui = DirectUIForDelete("alimentació", confirmacio=True)  # Different case
    cas_us = EliminarCategoria(fake_repo, ui)

    # --- Act ---
    result = cas_us.execute()

    # --- Assert ---
    assert result is False  # Should not find the category due to case sensitivity
    assert len(fake_repo.categories) == 1  # Category should still exist


class DirectUI:
    """UI implementation that returns predefined values for testing direct execution"""

    def __init__(self, nom_categoria, confirmacio=True):
        self.nom_categoria = nom_categoria
        self.confirmacio = confirmacio
        self.call_count = 0
        self.popup_messages = []  # Track popup messages for testing

    def input_popup(self, text, title, default_text=None):
        """Return predefined values based on the call sequence"""
        # This method is not used for elimination, but we include it for consistency
        return None

    def mostrar_popup(self, titol, text):
        """Track popup messages for testing purposes"""
        self.popup_messages.append((titol, text))

    def confirmar_accio(self, missatge):
        """Return predefined confirmation value for testing"""
        return self.confirmacio


def test_eliminar_categoria_removes_existing_category_through_ui():
    """Test that EliminarCategoria removes an existing category from the repository when using UI"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    ui = DirectUIForDelete("transport", confirmacio=True)
    cas_us = EliminarCategoria(fake_repo, ui)

    # --- Act ---
    result = cas_us.execute()

    # --- Assert ---
    assert result is True  # Indicating success
    assert "transport" not in fake_repo.categories
    assert len(fake_repo.categories) == 2  # Only 2 categories should remain
    # Verify other categories remain unchanged
    assert "alimentació" in fake_repo.categories
    assert "habitatge" in fake_repo.categories


def test_eliminar_categoria_handles_cancelled_confirmation():
    """Test that EliminarCategoria handles cancelled confirmation appropriately"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    ui = DirectUI("transport", confirmacio=False)  # User cancelled
    cas_us = EliminarCategoria(fake_repo, ui)

    # --- Act ---
    result = cas_us.execute()

    # --- Assert ---
    assert result is False  # Indicating cancellation
    assert "transport" in fake_repo.categories  # Category should still exist
    assert len(fake_repo.categories) == 3  # No categories should be removed


class MockUI:
    """Mock UI for testing that simulates the UI interaction"""

    def __init__(self, nom_categoria_retorn=None, confirmacio_retorn=True):
        self.nom_categoria_retorn = nom_categoria_retorn
        self.confirmacio_retorn = confirmacio_retorn
        self.input_calls = []  # To track calls to input_popup
        self.popup_messages = []  # Track popup messages for testing
        self.confirmation_calls = []  # Track confirmation calls

    def input_popup(self, text, title, default_text=None):
        """Simulate UI popup that gets user input"""
        self.input_calls.append((text, title, default_text))
        return self.nom_categoria_retorn

    def mostrar_popup(self, titol, text):
        """Track popup messages for testing purposes"""
        self.popup_messages.append((titol, text))

    def confirmar_accio(self, missatge):
        """Track confirmation calls for testing purposes"""
        self.confirmation_calls.append(missatge)
        return self.confirmacio_retorn


def test_eliminar_categoria_interacts_with_ui():
    """Test that EliminarCategoria interacts with UI to get user input and confirmation"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    mock_ui = MockUI(nom_categoria_retorn="transport", confirmacio_retorn=True)
    cas_us = EliminarCategoria(fake_repo, mock_ui)

    # --- Act ---
    result = cas_us.execute()

    # --- Assert ---
    assert result is True  # Operation should succeed
    assert "transport" not in fake_repo.categories  # Category should be removed
    assert len(mock_ui.input_calls) == 1  # One call to input_popup for category name
    assert len(mock_ui.confirmation_calls) == 1  # One call to confirm deletion
    assert len(mock_ui.popup_messages) == 1  # One success message
    assert mock_ui.popup_messages[0][0] == "Èxit"  # Title should be "Èxit"