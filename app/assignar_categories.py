from domain import calcular_stats, assignar_categories_a_moviments


class AssignarCategories:
    """
    Cas d'ús per tornar a assignar categories als moviments.
    Quan es tanca la finestra de categories, es tornen a assignar
    les categories als moviments segons les paraules clau actualitzades.
    """

    def __init__(self, repositori_moviments, ui, repositori_categories):
        self._repositori_moviments = repositori_moviments
        self._ui = ui
        self._repositori_categories = repositori_categories

    def execute(self):
        """
        Executa el cas d'ús per tornar a assignar categories als moviments.
        Obté els moviments actuals, els assigna les categories segons
        les paraules clau del repositori de categories i els torna a desar.
        """
        # 1️⃣ Obtenir tots els moviments actuals
        moviments = self._repositori_moviments.obtenir_tots()

        # 2️⃣ Assignar categories als moviments segons les paraules clau
        moviments_amb_categories = assignar_categories_a_moviments(moviments, self._repositori_categories)

        # 3️⃣ Desar els moviments actualitzats
        self._repositori_moviments.save(moviments_amb_categories)

        # 4️⃣ Calcular estadístiques
        moviments_per_estadistiques = self._repositori_moviments.obtenir_tots()
        moviments_per_estadistiques = sorted(moviments_per_estadistiques, key=lambda m: (m.data, m.banc))
        total, diari, mensual = calcular_stats(moviments_per_estadistiques)

        # 5️⃣ Actualitzar la UI amb els moviments actualitzats
        self._ui.mostrar_moviments(moviments_per_estadistiques, total, round(diari, 2), round(mensual, 2))