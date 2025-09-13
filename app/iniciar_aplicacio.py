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
        print('afegir_categories')
        cats = repo_cats.get_all()
        for m in moviments:
            for cat in cats.keys():
                texts = cats[cat]
                for t in texts:
                    if t in m.concepte:
                        m.categoria = cat
                        break
        return moviments
        
    def execute(self):
        """
        Obté els moviments del repositori i actualitza la UI.
        """
        moviments = self._repositori.obtenir_tots()
        movs = self.afegir_moviments_ficticis(moviments)
        self._repositori.enriquir(movs)
        moviments = self._repositori.obtenir_tots()
        movs = self.afegir_categories(moviments, self._repositori_cats)
        self._repositori.save(movs)
        moviments = self._repositori.obtenir_tots()
        moviments = sorted(moviments, key=lambda m: (m.data,m.banc))
        
        total, diari, mensual = calcular_stats(moviments)
        
        # La UI hauria de tenir un mètode mostrar_moviments
        self._ui.mostrar_moviments(moviments, total, round(diari,2), round(mensual,2))
        # Si és una UI Textual, llavors cridem run() per iniciar l'app
        if hasattr(self._ui, "run"):
            self._ui.run()
