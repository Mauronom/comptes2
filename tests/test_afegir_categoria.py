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


class DirectUI:
    """UI implementation that returns predefined values for testing direct execution"""

    def __init__(self, nom_categoria, paraules_clau):
        self.nom_categoria = nom_categoria
        self.paraules_clau = paraules_clau
        self.call_count = 0
        self.popup_messages = []  # Track popup messages for testing
        self.actualitzar_categories_called = False  # Track if method was called

    def input_popup(self, text, title):
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


def test_afegir_categoria_creates_new_category():
    """Test that AfegirCategoria creates a new category in the repository"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    ui = DirectUI("alimentació", ["supermercat", "fruits", "verdures"])
    cas_us = AfegirCategoria(fake_repo, ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert "alimentació" in fake_repo.categories
    assert fake_repo.categories["alimentació"] == ["supermercat", "fruits", "verdures"]
    assert ui.actualitzar_categories_called  # Verify that the method was called


def test_afegir_categoria_overwrites_existing_category():
    """Test that AfegirCategoria overwrites an existing category"""
    # --- Arrange ---
    initial_categories = {"transport": ["gasolina", "autobús"]}
    fake_repo = FakeCategoriesRepo(initial_categories)
    ui = DirectUI("transport", ["taxi", "metro"])
    cas_us = AfegirCategoria(fake_repo, ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert "transport" in fake_repo.categories
    assert fake_repo.categories["transport"] == ["taxi", "metro"]


def test_afegir_categoria_with_empty_keywords():
    """Test that AfegirCategoria can handle empty keywords list"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    ui = DirectUI("categoria_buida", [])
    cas_us = AfegirCategoria(fake_repo, ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert "categoria_buida" in fake_repo.categories
    assert fake_repo.categories["categoria_buida"] == []


def test_afegir_categoria_with_special_characters():
    """Test that AfegirCategoria handles special characters correctly"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    ui = DirectUI("ocasió especial", ["café", "naïf", "fiançailles"])
    cas_us = AfegirCategoria(fake_repo, ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert "ocasió especial" in fake_repo.categories
    assert fake_repo.categories["ocasió especial"] == ["café", "naïf", "fiançailles"]


class MockUI:
    """Mock UI for testing that simulates the UI interaction"""

    def __init__(self, nom_categoria_retorn=None, paraules_clau_retorn=None):
        self.nom_categoria_retorn = nom_categoria_retorn
        self.paraules_clau_retorn = paraules_clau_retorn
        self.input_calls = []  # To track calls to input_popup
        self.popup_messages = []  # Track popup messages for testing
        self.actualitzar_categories_called = False  # Track if method was called

    def input_popup(self, text, title):
        """Simulate UI popup that gets user input"""
        self.input_calls.append((text, title))

        if len(self.input_calls) == 1:  # First call is for category name
            return self.nom_categoria_retorn
        elif len(self.input_calls) == 2:  # Second call is for keywords
            return self.paraules_clau_retorn
        return None

    def mostrar_popup(self, titol, text):
        """Track popup messages for testing purposes"""
        self.popup_messages.append((titol, text))

    def actualitzar_categories(self):
        """Simulate updating categories for testing purposes"""
        self.actualitzar_categories_called = True  # Mark that method was called


def test_afegir_categoria_interacts_with_ui():
    """Test that AfegirCategoria interacts with UI to get user input"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    mock_ui = MockUI(nom_categoria_retorn="alimentació", paraules_clau_retorn="supermercat, fruits, verdures")
    cas_us = AfegirCategoria(fake_repo, mock_ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert "alimentació" in fake_repo.categories
    assert fake_repo.categories["alimentació"] == ["supermercat", "fruits", "verdures"]
    assert len(mock_ui.input_calls) == 2  # Two calls to UI: one for category name, one for keywords
    assert mock_ui.input_calls[0] == ("Nom de la nova categoria:", "Nova Categoria")
    assert mock_ui.input_calls[1] == ("Paraules clau separades per comes:", "Paraules Clau")
    assert mock_ui.actualitzar_categories_called  # Verify that the method was called


def test_afegir_categoria_handles_none_category_input():
    """Test that AfegirCategoria handles None category input gracefully"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    mock_ui = MockUI(nom_categoria_retorn=None, paraules_clau_retorn="some, keywords")
    cas_us = AfegirCategoria(fake_repo, mock_ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert len(fake_repo.categories) == 0  # No category should be added
    assert len(mock_ui.input_calls) == 1  # Only first call should happen
    # Note: actualitzar_categories is NOT called when no category name is provided
    assert not mock_ui.actualitzar_categories_called  # Verify that the method was NOT called when no category is provided


def test_afegir_categoria_handles_none_keywords_input():
    """Test that AfegirCategoria handles None keywords input gracefully"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    mock_ui = MockUI(nom_categoria_retorn="categoria_prova", paraules_clau_retorn=None)
    cas_us = AfegirCategoria(fake_repo, mock_ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert "categoria_prova" in fake_repo.categories
    assert fake_repo.categories["categoria_prova"] == []
    assert len(mock_ui.input_calls) == 2  # Both calls should happen
    assert mock_ui.actualitzar_categories_called  # Verify that the method was called


def test_afegir_categoria_processes_keywords_correctly():
    """Test that AfegirCategoria correctly processes keywords from comma-separated string"""
    # --- Arrange ---
    fake_repo = FakeCategoriesRepo()
    mock_ui = MockUI(nom_categoria_retorn="transport", paraules_clau_retorn="gasolina, autobús, taxi")
    cas_us = AfegirCategoria(fake_repo, mock_ui)

    # --- Act ---
    cas_us.execute()

    # --- Assert ---
    assert "transport" in fake_repo.categories
    assert fake_repo.categories["transport"] == ["gasolina", "autobús", "taxi"]
    assert len(mock_ui.input_calls) == 2
    assert mock_ui.actualitzar_categories_called  # Verify that the method was called