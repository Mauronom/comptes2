from domain import Moviment, calcular_stats
import datetime

class IniciarAplicacio:
    def __init__(self, repositori_moviments, ui, repositori_cats, extra_moves=[]):
        self._repositori = repositori_moviments
        self._repositori_cats = repositori_cats
        self._ui = ui
        self.extra_moves = extra_moves
        

    def afegir_moviments_ficticis(self, moviments):
        movs = Moviment.clone_list(self.extra_moves)
        for m in moviments:
            if "R/ Caja de Ingenieros Vida " in m.concepte or "PLAN AHORRO 5 SIALP" in m.concepte or "CI PIAS" in m.concepte:
                movs.append(Moviment(
                    data=m.data,
                    concepte="SIALP PIES",
                    import_=-m.import_,
                    balance=-m.import_ if not movs else movs[-1].balance - m.import_,
                    banc="SIALP_PIAS"
                ))
        return movs

    def afegir_categories(self, moviments, repo_cats):
        cats = repo_cats.get_all()
        for m in moviments:
            for cat in cats.keys():
                texts = cats[cat]
                for t in texts:
                    if t.lower() in m.concepte.lower():
                        m.categoria = cat
                        break
        return moviments
        
    def execute(self):
        """
        Demana el directori a la UI, obté els moviments del repositori i actualitza la UI.
        """
        # 1️⃣ Demanar directori a la UI
        directori = self._ui.demanar_directori()

        # 2️⃣ Carregar moviments del repositori
        moviments = self._repositori.obtenir_tots(directori)

        # 3️⃣ Afegir moviments ficticis
        movs = self.afegir_moviments_ficticis(moviments)
        self._repositori.enriquir(movs)

        # 4️⃣ Afegir categories
        moviments = self._repositori.obtenir_tots(directori)
        movs = self.afegir_categories(moviments, self._repositori_cats)
        self._repositori.save(movs)

        # 5️⃣ Preparar moviments finals
        moviments = self._repositori.obtenir_tots(directori)
        moviments = sorted(moviments, key=lambda m: (m.data, m.banc))
        
        total, diari, mensual = calcular_stats(moviments)
        
        # 6️⃣ Mostrar resultats a la UI
        self._ui.mostrar_moviments(moviments, total, round(diari, 2), round(mensual, 2))

        # 7️⃣ Si és una UI interactiva, arrencar-la
        if hasattr(self._ui, "run"):
            self._ui.run()
