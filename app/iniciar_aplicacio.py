# app.py (modificada)
from domain import Moviment, calcular_stats, ConfigMovimentsFicticisRepo
import datetime

class IniciarAplicacio:
    def __init__(self, repositori_moviments, ui, repositori_cats, 
                 repositori_config_ficticis: ConfigMovimentsFicticisRepo = None, 
                 extra_moves=[]):
        self._repositori = repositori_moviments
        self._repositori_cats = repositori_cats
        self._ui = ui
        self._repositori_config_ficticis = repositori_config_ficticis
        self.extra_moves = extra_moves
        

    def afegir_moviments_ficticis(self, moviments):
        movs = Moviment.clone_list(self.extra_moves)
        
        if self._repositori_config_ficticis is None:
            return movs
            
        regles = self._repositori_config_ficticis.get_regles()
        
        for m in moviments:
            for regla in regles:
                if self._coincideix_patrons(m.concepte, regla.patrons):
                    import_final = -m.import_ if regla.invertir_import else m.import_
                    balance_final = import_final if not movs else movs[-1].balance + import_final
                    
                    movs.append(Moviment(
                        data=m.data,
                        concepte=regla.concepte_desti,
                        import_=import_final,
                        balance=balance_final,
                        banc=regla.banc_desti
                    ))
                    break  # Només aplica la primera regla que coincideixi
        
        return movs
    
    def _coincideix_patrons(self, concepte, patrons):
        return any(patro in concepte for patro in patrons)

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