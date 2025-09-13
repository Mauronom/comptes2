from datetime import datetime, date
from domain import Moviment, calcular_stats

class FiltrarMoviments:
    def __init__(self, repositori, ui):
        self._repositori = repositori
        self._ui = ui

    def execute(self, text: str, data_inici: str = "", data_fi: str = "", categoria: str = "Totes"):
        """Filtra els moviments per concepte i dates, i actualitza la UI."""
        moviments = self._repositori.obtenir_tots()
        
        # Aplicar filtre de text
        text = (text or "").lower()
        if text:
            moviments = [
                m for m in moviments
                if text in m.concepte.lower()
            ]
        if categoria and categoria != "Totes":
            moviments = [
                m for m in moviments
                if m.categoria == categoria
            ]
        # Convertir strings a objectes date
        date_inici = self._convertir_string_a_date(data_inici.strip())
        date_fi = self._convertir_string_a_date(data_fi.strip())
        
        # Aplicar filtres de data
        moviments = self._filtrar_per_dates(moviments, date_inici, date_fi)
        
        total, diari, mensual = calcular_stats(moviments, date_inici, date_fi)
        self._ui.mostrar_moviments(moviments, total, round(diari,2), round(mensual,2))

    def _filtrar_per_dates(self, moviments, date_inici: date, date_fi: date):
        """Filtra els moviments per rang de dates."""
        
        # Si les dates no són vàlides, retornar tots els moviments
        if not date_inici and not date_fi:
            return moviments
            
        # Si data inici és posterior a data fi, retornar llista buida
        if date_inici and date_fi and date_inici > date_fi:
            return []

        # Aplicar filtres de data
        moviments_filtrats = []
        for moviment in moviments:
            # Comprovar data d'inici
            if date_inici and moviment.data < date_inici:
                continue
                
            # Comprovar data de fi
            if date_fi and moviment.data > date_fi:
                continue
                
            moviments_filtrats.append(moviment)
            
        return moviments_filtrats

    def _convertir_string_a_date(self, data_str: str):
        """Converteix un string en format YYYY-MM-DD a objecte date."""
        if not data_str:
            return None
            
        try:
            return datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            return None  # Data amb format incorrecte