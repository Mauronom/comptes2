from .memory_repositori_categories import MemoryCategoriesRepo

class RepositoriCategoria(MemoryCategoriesRepo):
    
    def __init__(self, directori):
        import json
        self.directori = directori
        with open(f'{self.directori}/categories.json', 'r') as fitxer:
            self.categories = json.load(fitxer)
        
    def save(self,name,texts):
        import json
        self.categories[name] = texts
        with open(f'{self.directori}/categories.json', 'w') as fitxer:
            json.dump(self.categories, fitxer, indent=2, ensure_ascii=False)
