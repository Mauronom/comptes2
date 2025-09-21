# config_repo.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict
import json
from domain import ConfigMovimentsFicticisRepo, ReglaMovimentFictici


class JsonConfigMovimentsFicticisRepo(ConfigMovimentsFicticisRepo):
    def __init__(self, config_path):
        self.config_path = config_path
    
    def get_regles(self) -> List[ReglaMovimentFictici]:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            regles = []
            for nom_regla, regla_data in config.get("moviments_ficticis", {}).items():
                regles.append(ReglaMovimentFictici(
                    patrons=regla_data["patrons"],
                    concepte_desti=regla_data["concepte_desti"],
                    banc_desti=regla_data["banc_desti"],
                    invertir_import=regla_data.get("invertir_import", True)
                ))
            return regles
        except FileNotFoundError:
            print(f"Warning: Config file {self.config_path} not found. No fictitious movement rules loaded.")
            return []

class MemoryConfigMovimentsFicticisRepo(ConfigMovimentsFicticisRepo):
    def __init__(self, regles: List[ReglaMovimentFictici] = None):
        self._regles = regles or []
    
    def get_regles(self) -> List[ReglaMovimentFictici]:
        return self._regles.copy()
    
    def afegir_regla(self, regla: ReglaMovimentFictici):
        self._regles.append(regla)