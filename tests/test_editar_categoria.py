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


class DirectUI:
    """UI implementation that returns predefined values for testing direct execution"""

    def __init__(self, nom_categoria, paraules_clau):
        self.nom_categoria = nom_categoria
        self.paraules_clau = paraules_clau
        self.call_count = 0
        self.popup_messages = []  # Track popup messages for testing
        self.actualitzar_categories_called = False  # Track if method was called

    def input_popup(self, text, title, default_text=None):
        """Return predefined values based on the call sequence"""
        self.call_count += 1
        if self.call_count == 1:  # First call is for category name
            if isinstance(self.nom_categoria, str):
                return self.nom_categoria
            elif isinstance(self.nom_categoria, list) and len(self.nom_categoria) > 0:
                return self.nom_categoria[0]  # Take first element if it's a list
            else:
                return str(self.nom_categoria) if self.nom_categoria is not None else None
        elif self.call_count == 2:  # Second call is for keywords
            if isinstance(self.paraules_clau, list):
                return ", ".join(self.paraules_clau)
            else:
                return str(self.paraules_clau) if self.paraules_clau is not None else None
        return None

    def mostrar_popup(self, titol, text):
        """Track popup messages for testing purposes"""
        self.popup_messages.append((titol, text))

    def actualitzar_categories(self):
        """Simulate updating categories for testing purposes"""
        self.actualitzar_categories_called = True  # Mark that method was called


def test_editar_categoria_updates_existing_category():
    """Test that EditarCategoria updates an existing category in the repository"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    ui = DirectUI("alimentació", ["carn", "peix", "ous"], ["alimentació", "transport", "habitatge"])
    cas_us = EditarCategoria(fake_repo, ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert "alimentació" in fake_repo.categories
    assert fake_repo.categories["alimentació"] == ["carn", "peix", "ous"]
    # Verify other categories remain unchanged
    assert "transport" in fake_repo.categories
    assert fake_repo.categories["transport"] == ["gasolina", "autobús", "tren"]
    assert ui.actualitzar_categories_called  # Verify that the method was called


def test_editar_categoria_creates_new_category():
    """Test that EditarCategoria creates a new category if it doesn't exist"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    ui = DirectUI("ocidi", ["cinema", "teatre", "restaurants"])
    cas_us = EditarCategoria(fake_repo, ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert "ocidi" in fake_repo.categories
    assert fake_repo.categories["ocidi"] == ["cinema", "teatre", "restaurants"]
    # Verify other categories remain unchanged
    assert "alimentació" in fake_repo.categories
    assert ui.actualitzar_categories_called  # Verify that the method was called


def test_editar_categoria_with_empty_keywords():
    """Test that EditarCategoria can handle empty keywords list"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    ui = DirectUI("habitatge", [])
    cas_us = EditarCategoria(fake_repo, ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert "habitatge" in fake_repo.categories
    assert fake_repo.categories["habitatge"] == []
    assert ui.actualitzar_categories_called  # Verify that the method was called


def test_editar_categoria_with_special_characters():
    """Test that EditarCategoria handles special characters correctly"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    ui = DirectUI("ocasió especial", ["café", "naïf", "fiançailles"])
    cas_us = EditarCategoria(fake_repo, ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert "ocasió especial" in fake_repo.categories
    assert fake_repo.categories["ocasió especial"] == ["café", "naïf", "fiançailles"]
    assert ui.actualitzar_categories_called  # Verify that the method was called


class DirectUI:
    """UI implementation that returns predefined values for testing direct execution"""

    def __init__(self, nom_categoria, paraules_clau, categories_disponibles=None):
        self.nom_categoria = nom_categoria
        self.paraules_clau = paraules_clau
        self.categories_disponibles = categories_disponibles or []
        self.call_count = 0
        self.popup_messages = []  # Track popup messages for testing purposes
        self.actualitzar_categories_called = False  # Track if method was called

    def input_popup(self, text, title, default_text=None):
        """Return predefined values for keyword input"""
        # This is called for keywords input
        if isinstance(self.paraules_clau, list):
            return ", ".join(self.paraules_clau)
        else:
            return str(self.paraules_clau) if self.paraules_clau is not None else None

    def seleccionar_categoria(self, categories, missatge):
        """Return predefined selected category"""
        if isinstance(self.nom_categoria, str):
            return self.nom_categoria
        elif isinstance(self.nom_categoria, list) and len(self.nom_categoria) > 0:
            return self.nom_categoria[0]  # Take first element if it's a list
        else:
            return str(self.nom_categoria) if self.nom_categoria is not None else None

    def mostrar_popup(self, titol, text):
        """Track popup messages for testing purposes"""
        self.popup_messages.append((titol, text))

    def actualitzar_categories(self):
        """Simulate updating categories for testing purposes"""
        self.actualitzar_categories_called = True  # Mark that method was called


def test_editar_categoria_creates_new_category():
    """Test that EditarCategoria creates a new category in the repository when using UI"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    ui = DirectUI("nova_categoria", ["paraula1", "paraula2"], ["alimentació", "transport", "habitatge"])
    cas_us = EditarCategoria(fake_repo, ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert "nova_categoria" in fake_repo.categories
    assert fake_repo.categories["nova_categoria"] == ["paraula1", "paraula2"]
    assert ui.actualitzar_categories_called  # Verify that the method was called


def test_editar_categoria_updates_existing_category_through_ui():
    """Test that EditarCategoria updates an existing category when using UI"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    ui = DirectUI("alimentació", ["carn", "peix", "ous"], ["alimentació", "transport", "habitatge"])
    cas_us = EditarCategoria(fake_repo, ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert "alimentació" in fake_repo.categories
    assert fake_repo.categories["alimentació"] == ["carn", "peix", "ous"]
    assert ui.actualitzar_categories_called  # Verify that the method was called


class MockUI:
    """Mock UI for testing that simulates the UI interaction"""

    def __init__(self, nom_categoria_retorn=None, paraules_clau_retorn=None, categories_disponibles=None):
        self.nom_categoria_retorn = nom_categoria_retorn
        self.paraules_clau_retorn = paraules_clau_retorn
        self.categories_disponibles = categories_disponibles or []
        self.input_calls = []  # To track calls to input_popup
        self.seleccio_categoria_calls = []  # To track calls to seleccionar_categoria
        self.popup_messages = []  # Track popup messages for testing
        self.actualitzar_categories_called = False  # Track if method was called

    def input_popup(self, text, title, default_text=None):
        """Simulate UI popup that gets user input for keywords"""
        self.input_calls.append((text, title, default_text))
        # This is called for keywords input
        return self.paraules_clau_retorn

    def seleccionar_categoria(self, categories, missatge):
        """Simulate UI category selection"""
        self.seleccio_categoria_calls.append((categories, missatge))
        return self.nom_categoria_retorn

    def mostrar_popup(self, titol, text):
        """Track popup messages for testing purposes"""
        self.popup_messages.append((titol, text))

    def actualitzar_categories(self):
        """Simulate updating categories for testing purposes"""
        self.actualitzar_categories_called = True  # Mark that method was called


def test_editar_categoria_interacts_with_ui():
    """Test that EditarCategoria interacts with UI to get user input"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    mock_ui = MockUI(
        nom_categoria_retorn="transport",
        paraules_clau_retorn="taxi, metro, bicicleta",
        categories_disponibles=["alimentació", "transport", "habitatge"]
    )
    cas_us = EditarCategoria(fake_repo, mock_ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert "transport" in fake_repo.categories
    assert fake_repo.categories["transport"] == ["taxi", "metro", "bicicleta"]
    assert len(mock_ui.seleccio_categoria_calls) == 1  # One call to seleccionar_categoria
    assert len(mock_ui.input_calls) == 1  # One call to input_popup for keywords
    assert mock_ui.input_calls[0][:2] == ("Editar paraules clau:", "Editar Paraules Clau")
    assert len(mock_ui.popup_messages) == 1  # One success message
    assert mock_ui.popup_messages[0][0] == "Èxit"  # Title should be "Èxit"
    assert mock_ui.actualitzar_categories_called  # Verify that the method was called