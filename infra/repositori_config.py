
# config_repo.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict
import json
from datetime import datetime
from domain import ConfigMovimentsFicticisRepo, ReglaMovimentFictici


class JsonConfigMovimentsFicticisRepo(ConfigMovimentsFicticisRepo):
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
    
    def get_regles(self) -> List[ReglaMovimentFictici]:
        config = self._load_config()
        regles = []
        for nom_regla, regla_data in config.get("moviments_ficticis", {}).items():
            regles.append(ReglaMovimentFictici(
                patrons=regla_data["patrons"],
                concepte_desti=regla_data["concepte_desti"],
                banc_desti=regla_data["banc_desti"],
                invertir_import=regla_data.get("invertir_import", True)
            ))
        return regles
    
    def get_moviments_inicials(self) -> List:
        from domain import Moviment  # Importació dinàmica per evitar dependències circulars
        
        config = self._load_config()
        moviments = []
        for mov_data in config.get("moviments_inicials", []):
            # Convertir string de data a datetime.date
            data = datetime.strptime(mov_data["data"], "%Y-%m-%d").date()
            moviments.append(Moviment(
                data=data,
                concepte=mov_data["concepte"],
                import_=mov_data["import"],
                balance=mov_data["balance"],
                banc=mov_data["banc"]
            ))
        return moviments
    
    def _load_config(self) -> dict:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

class MemoryConfigMovimentsFicticisRepo(ConfigMovimentsFicticisRepo):
    def __init__(self, regles: List[ReglaMovimentFictici] = None, moviments_inicials: List = None):
        self._regles = regles or []
        self._moviments_inicials = moviments_inicials or []
    
    def get_regles(self) -> List[ReglaMovimentFictici]:
        return self._regles.copy()
    
    def get_moviments_inicials(self) -> List:
        return self._moviments_inicials.copy()
    
    def afegir_regla(self, regla: ReglaMovimentFictici):
        self._regles.append(regla)
    
    def afegir_moviment_inicial(self, moviment):
        self._moviments_inicials.append(moviment)