from datetime import datetime
from domain import Moviment

class UIFreeSimpleGUI:
    """UI amb FreeSimpleGUI: taula, filtre, log i botons de gràfiques"""

    def __init__(self, repositori_moviments, repositori_categories):
        import FreeSimpleGUI as sg
        self._repositori = repositori_moviments
        self._moviments = []
        self._cas_us_grafica_balance = None
        self._cas_us_grafica_imports = None
        self._cas_us_grafica_categories = None
        self._cas_us_filtrar_moviments = None

        # Definició de la interfície
        sg.set_options(font=('Arial', 20))  # Nom de la font i mida

        layout = [
            [sg.Text("Filtre:"), sg.Input(key="-INPUT_FILTRE-", enable_events=True),
             sg.Text("Categoria:"), sg.Combo(values=[], key="-COMBO_CATEGORIA-", enable_events=True, readonly=True, size=(15, 1))],
            [sg.Text("Data inici:"), 
             sg.Input(key="-DATA_INICI-", size=(12, 1), enable_events=True),
             sg.CalendarButton("📅", target="-DATA_INICI-", format="%Y-%m-%d", font=('Arial', 20)),
             sg.Text("Data fi:"),
             sg.Input(key="-DATA_FI-", size=(12, 1), enable_events=True),
             sg.CalendarButton("📅", target="-DATA_FI-", format="%Y-%m-%d", font=('Arial', 20))],
            [sg.Button("Mostrar gràfica per balanç", key="-BTN_BALANCE-"),
             sg.Button("Mostrar gràfica per imports", key="-BTN_IMPORTS-"),
             sg.Button("Mostrar gràfica per categories", key="-BTN_CATEGORIES-"),
             sg.Button("Gestionar Categories", key="-BTN_GESTIONAR_CATEGORIES-")],
            [sg.Table(values=[],
                      headings=["Data", "Concepte", "Import (€)", "Balanç", "Banc", 'Categoria'],
                      auto_size_columns=True,
                      justification="left",
                      key="-TAULA-",
                      expand_x=True,
                      expand_y=True,
                      enable_events=True,
                      num_rows=8)],
            [sg.Table(values=[],
                      headings=["Data", "Concepte", "Import (€)", "Balanç", "Banc", 'Categoria'],
                      auto_size_columns=True,
                      justification="left",
                      key="-TAULA2-",
                      expand_x=True,
                      expand_y=True,
                      enable_events=True,
                      num_rows=8)],
            [sg.Text("Total: "), sg.Text("0.00", key="-Total-"),
             sg.Text("Diari: "), sg.Text("0.00", key="-Diari-"),
             sg.Text("Mensual: "), sg.Text("0.00", key="-Mensual-")],
        ]
        self.window = sg.Window("Moviments Bancaris", layout, finalize=True, resizable=True, size=(1200, 700))
        categories = list(repositori_categories.get_all().keys())+["altres","Totes"]
        self.window["-COMBO_CATEGORIA-"].update(values=categories, value="Totes")

    def demanar_directori(self):
        """Demana a l’usuari el directori on hi ha els fitxers Norma43."""
        import FreeSimpleGUI as sg
        directori = sg.popup_get_folder("Selecciona el directori amb els fitxers Norma43",
                                        default_path="infra/dades/",
                                        no_window=False)
        # Si l’usuari cancel·la, retornem el path per defecte
        return directori or "infra/dades/"

    def set_casos_us(self, cas_us_grafica_balance, cas_us_grafica_imports, cas_us_filtrar_moviments, cas_us_grafica_categories, cas_us_mostrar_categories=None, cas_us_afegir_categoria=None, cas_us_editar_categoria=None, cas_us_eliminar_categoria=None):
        self._cas_us_grafica_balance = cas_us_grafica_balance
        self._cas_us_grafica_imports = cas_us_grafica_imports
        self._cas_us_filtrar_moviments = cas_us_filtrar_moviments
        self._cas_us_grafica_categories = cas_us_grafica_categories
        self._cas_us_mostrar_categories = cas_us_mostrar_categories
        self._cas_us_afegir_categoria = cas_us_afegir_categoria
        self._cas_us_editar_categoria = cas_us_editar_categoria
        self._cas_us_eliminar_categoria = cas_us_eliminar_categoria

    def print(self, info):
        """Escriu al log (equivalent al print de Textual)."""
        text = str(info) + "\n"
        log = self.window["-LOG-"]
        log.update(log.get() + text)

    def mostrar_moviments(self, moviments, total, diari, mensual):
        """Actualitza la taula amb els moviments."""
        self._moviments = moviments
        taula = self.window["-TAULA-"]
        dades = [[str(m.data), m.concepte, f"{m.import_:.2f}", m.balance, m.banc, m.categoria] for m in moviments]
        taula.update(values=dades)
        taula = self.window["-TAULA2-"]
        moviments2 = Moviment.clone_list(moviments)
        moviments2 = sorted(moviments2, key=lambda m: (m.import_,m.data))
        dades = [[str(m.data), m.concepte, f"{m.import_:.2f}", m.balance, m.banc, m.categoria] for m in moviments2]
        taula.update(values=dades)
        w_total = self.window["-Total-"]
        w_total.update(str(total))
        w_diari = self.window["-Diari-"]
        w_diari.update(str(diari))
        w_mensual = self.window["-Mensual-"]
        w_mensual.update(str(mensual))

    def mostrar_categories(self, categories):
        """Mostra una finestra amb la llista de categories i permet gestionar-les."""
        import FreeSimpleGUI as sg

        # Preparar les dades per a la taula
        # Guardem tant la llista original com la versió en cadena per a la UI
        table_data = []
        original_keywords = {}  # Diccionari per mantenir les llistes originals
        for category, keywords in categories.items():
            keywords_str = ", ".join(keywords)
            table_data.append([category, keywords_str])
            original_keywords[category] = keywords  # Guardem la llista original

        # Crear el layout per a la finestra de categories
        layout = [
            [sg.Text("Gestió de Categories", font=("Arial", 16))],
            [sg.Table(
                values=table_data,
                headings=["Categoria", "Paraules clau associades"],
                col_widths=[20, 50],
                auto_size_columns=False,
                justification="left",
                key="-TABLE_CATEGORIES-",
                expand_x=True,
                expand_y=True,
                num_rows=min(len(table_data), 10)  # Mostrar fins a 10 files
            )],
            [sg.Button("Afegir Categoria", key="-BTN_AFEGIR-"),
             sg.Button("Editar Categoria", key="-BTN_EDITAR-"),
             sg.Button("Eliminar Categoria", key="-BTN_ELIMINAR-"),
             sg.Button("Tancar", key="-BTN_TANCAR-")]
        ]

        # Crear la finestra modal
        window = sg.Window("Gestió de Categories", layout, modal=True, finalize=True, resizable=True, size=(800, 400))

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == "-BTN_TANCAR-":
                break
            elif event == "-BTN_AFEGIR-":
                # Diàleg per afegir nova categoria
                nova_categoria = sg.popup_get_text("Nom de la nova categoria:", title="Nova Categoria")
                if nova_categoria:
                    paraules_clau = sg.popup_get_text("Paraules clau separades per comes:", title="Paraules Clau")
                    if paraules_clau:
                        # Convertir la cadena de paraules clau en una llista
                        paraules_clau_list = [p.strip() for p in paraules_clau.split(",") if p.strip()]
                        # Executar el cas d'ús per afegir la categoria
                        if hasattr(self, '_cas_us_afegir_categoria') and self._cas_us_afegir_categoria:
                            self._cas_us_afegir_categoria.execute(nova_categoria, paraules_clau_list)
                            # Actualitzar la visualització
                            sg.popup(f"S'ha afegit la categoria '{nova_categoria}' amb paraules clau: {paraules_clau}")
                            # Actualitzar la taula amb la nova categoria
                            table_data.append([nova_categoria, paraules_clau])
                            original_keywords[nova_categoria] = paraules_clau_list
                            window["-TABLE_CATEGORIES-"].update(values=table_data)
            elif event == "-BTN_EDITAR-":
                # Obtenir la fila seleccionada
                selected_rows = values["-TABLE_CATEGORIES-"]
                if selected_rows:
                    row_index = selected_rows[0]  # Agafem la primera fila seleccionada
                    if 0 <= row_index < len(table_data):
                        categoria_actual = table_data[row_index][0]

                        # Recuperem la llista original de paraules clau
                        paraules_originals = original_keywords.get(categoria_actual, [])
                        paraules_actuals = ", ".join(paraules_originals)  # Convertim a cadena per mostrar a la UI

                        # Diàleg per editar la categoria
                        nova_categoria = sg.popup_get_text("Editar categoria:", default_text=categoria_actual, title="Editar Categoria")
                        if nova_categoria:
                            noves_paraules = sg.popup_get_text("Editar paraules clau:", default_text=paraules_actuals, title="Editar Paraules Clau")
                            if noves_paraules:
                                # Convertir la cadena de paraules clau en una llista
                                noves_paraules_list = [p.strip() for p in noves_paraules.split(",") if p.strip()]
                                # Executar el cas d'ús per editar la categoria
                                if hasattr(self, '_cas_us_editar_categoria') and self._cas_us_editar_categoria:
                                    self._cas_us_editar_categoria.execute(nova_categoria, noves_paraules_list)
                                    # Actualitzar la visualització
                                    sg.popup(f"S'ha editat la categoria '{nova_categoria}' amb paraules clau: {noves_paraules}")
                                    # Actualitzar la taula amb les dades editades
                                    table_data[row_index] = [nova_categoria, noves_paraules]
                                    original_keywords[nova_categoria] = noves_paraules_list
                                    window["-TABLE_CATEGORIES-"].update(values=table_data)
            elif event == "-BTN_ELIMINAR-":
                # Obtenir la fila seleccionada
                selected_rows = values["-TABLE_CATEGORIES-"]
                if selected_rows:
                    row_index = selected_rows[0]  # Agafem la primera fila seleccionada
                    if 0 <= row_index < len(table_data):
                        categoria_a_eliminar = table_data[row_index][0]
                        confirmacio = sg.popup_yes_no(f"Segur que vol eliminar la categoria '{categoria_a_eliminar}'?")
                        if confirmacio == "Yes":
                            # Executar el cas d'ús per eliminar la categoria
                            if hasattr(self, '_cas_us_eliminar_categoria') and self._cas_us_eliminar_categoria:
                                result = self._cas_us_eliminar_categoria.execute(categoria_a_eliminar)
                                if result:
                                    # Eliminar la fila de la taula
                                    table_data.pop(row_index)
                                    if categoria_a_eliminar in original_keywords:
                                        del original_keywords[categoria_a_eliminar]
                                    window["-TABLE_CATEGORIES-"].update(values=table_data)
                                    sg.popup(f"S'ha eliminat la categoria '{categoria_a_eliminar}' correctament.")
                                else:
                                    sg.popup_error(f"No s'ha pogut eliminar la categoria '{categoria_a_eliminar}'.")

        window.close()

    def _aplicar_filtres(self):
        """Aplica els filtres quan canvien les dates o el text."""
        if self._cas_us_filtrar_moviments:
            data_inici = self.window["-DATA_INICI-"].get().strip()
            data_fi = self.window["-DATA_FI-"].get().strip()
            filtre_text = self.window["-INPUT_FILTRE-"].get()
            categoria_seleccionada = self.window["-COMBO_CATEGORIA-"].get()

            self._cas_us_filtrar_moviments.execute(filtre_text, data_inici, data_fi, categoria_seleccionada)

    def _validar_format_data(self, data_str):
        """Valida que la data tingui el format correcte YYYY-MM-DD."""
        if not data_str:
            return True
        try:
            datetime.strptime(data_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def run(self):
        import FreeSimpleGUI as sg
        """Bucle principal de l'app PySimpleGUI."""
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break

            if event == "-BTN_BALANCE-" and self._cas_us_grafica_balance:
                self._cas_us_grafica_balance.execute(self._moviments)

            elif event == "-BTN_IMPORTS-" and self._cas_us_grafica_imports:
                self._cas_us_grafica_imports.execute(self._moviments)
            elif event == "-BTN_CATEGORIES-" and self._cas_us_grafica_categories:
                self._cas_us_grafica_categories.execute(self._moviments)
            elif event == "-BTN_GESTIONAR_CATEGORIES-" and self._cas_us_mostrar_categories:
                self._cas_us_mostrar_categories.execute()
            elif event in ["-INPUT_FILTRE-", "-DATA_INICI-", "-DATA_FI-"]:
                data_inici = values.get("-DATA_INICI-", "").strip()
                data_fi = values.get("-DATA_FI-", "").strip()

                if self._validar_format_data(data_inici) and self._validar_format_data(data_fi):
                    self._aplicar_filtres()
            elif event == "-COMBO_CATEGORIA-":
                self._aplicar_filtres()

        self.window.close()
