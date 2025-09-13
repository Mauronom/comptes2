class MemoryCategoriesRepo:
    
    def __init__(self, cats={}):
        self.categories=cats
    
    def get_all(self,):
        return self.categories

    def find_by_name(self,name):
        return self.categories[name]

    def save(self,name,texts):...


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
