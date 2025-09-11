import FreeSimpleGUI as sg


class UIFreeSimpleGUI:
    """UI amb FreeSimpleGUI: taula, filtre, log i botons de gràfiques"""

    def __init__(self, repositori_moviments):
        self._repositori = repositori_moviments
        self._moviments = []
        self._cas_us_grafica_balance = None
        self._cas_us_grafica_imports = None
        self._cas_us_filtrar_moviments = None

        # Definició de la interfície
        layout = [
            [sg.Text("Filtre:"), sg.Input(key="-INPUT_FILTRE-", enable_events=True)],
            [sg.Button("Mostrar gràfica per balanç", key="-BTN_BALANCE-"),
             sg.Button("Mostrar gràfica per imports", key="-BTN_IMPORTS-")],
            [sg.Table(values=[],
                      headings=["Data", "Concepte", "Import (€)", "Balance", "Banc"],
                      auto_size_columns=True,
                      justification="left",
                      key="-TAULA-",
                      expand_x=True,
                      expand_y=True,
                      enable_events=True,
                      num_rows=15)],
            [sg.Multiline(size=(80, 10), key="-LOG-", autoscroll=True, disabled=True)]
        ]

        self.window = sg.Window("Moviments Bancaris", layout, finalize=True, resizable=True)

    def set_casos_us(self, cas_us_grafica_balance, cas_us_grafica_imports, cas_us_filtrar_moviments):
        self._cas_us_grafica_balance = cas_us_grafica_balance
        self._cas_us_grafica_imports = cas_us_grafica_imports
        self._cas_us_filtrar_moviments = cas_us_filtrar_moviments

    def print(self, info):
        """Escriu al log (equivalent al print de Textual)."""
        text = str(info) + "\n"
        log = self.window["-LOG-"]
        log.update(log.get() + text)

    def mostrar_moviments(self, moviments):
        """Actualitza la taula amb els moviments."""
        self._moviments = moviments
        taula = self.window["-TAULA-"]
        dades = [[str(m.data), m.concepte, f"{m.import_:.2f}", m.balance, m.banc] for m in moviments]
        taula.update(values=dades)

    def run(self):
        """Bucle principal de l'app PySimpleGUI."""
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break

            if event == "-BTN_BALANCE-" and self._cas_us_grafica_balance:
                self._cas_us_grafica_balance.execute(self._moviments)

            elif event == "-BTN_IMPORTS-" and self._cas_us_grafica_imports:
                self._cas_us_grafica_imports.execute(self._moviments)

            elif event == "-INPUT_FILTRE-" and self._cas_us_filtrar_moviments:
                self._cas_us_filtrar_moviments.execute(values["-INPUT_FILTRE-"])

        self.window.close()
