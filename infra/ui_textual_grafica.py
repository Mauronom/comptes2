from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Button, Input, Log
from textual.containers import Container, Horizontal

class UITextualGrafica(App):
    """UI Textual amb taula i botó per mostrar gràfica."""

    CSS_PATH = None

    def __init__(self, repositori_moviments):
        super().__init__()
        self.taula = None
        self._repositori = repositori_moviments
        self._moviments = []

    def set_casos_us(self, cas_us_grafica_balance, cas_us_grafica_imports, cas_us_filtrar_moviments):
        self._cas_us_grafica_balance = cas_us_grafica_balance
        self._cas_us_grafica_imports = cas_us_grafica_imports
        self._cas_us_filtrar_moviments = cas_us_filtrar_moviments

    def print(self,info):
        text = str(info)
        log = self.query_one("#log", Log)
        log.write(text+'\n')   # “com un print”

    def mostrar_moviments(self, moviments):
        """Mètode perquè el cas d'ús IniciarAplicació li passi els moviments."""
        self._moviments = moviments
        if self.taula:
            self.taula.clear()
            self.taula.add_columns("Data", "Concepte", "Import (€)", "Balance", "Banc")
            for m in self._moviments:
                self.taula.add_row(str(m.data), m.concepte, f"{m.import_:.2f}", m.balance, m.banc)

    def compose(self) -> ComposeResult:
        yield Log(id="log")
        yield Header()
        yield Input(placeholder="Filtre", id="input_filtre")
        yield Button("Mostrar gràfica per balanç", id="btn_grafica_balance")
        yield Button("Mostrar gràfica per imports", id="btn_grafica_imports")
        yield Container(DataTable(id="taula_moviments"))
        yield Footer()

    def on_mount(self):
        if not self.taula:
            self.taula = self.query_one("#taula_moviments", DataTable)
            self.taula.add_columns("Data", "Concepte", "Import (€)", "Balance", "Banc")
            for m in self._moviments:
                self.taula.add_row(str(m.data), m.concepte, f"{m.import_:.2f}", m.balance, m.banc)


    async def on_button_pressed(self, event):
        if event.button.id == "btn_grafica_balance":
            self._cas_us_grafica_balance.execute(self._moviments)
        if event.button.id == "btn_grafica_imports":
            self._cas_us_grafica_imports.execute(self._moviments)

    async def on_input_changed(self, event: Input.Changed):
        self._cas_us_filtrar_moviments.execute(event.value)