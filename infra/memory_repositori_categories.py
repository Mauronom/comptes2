class MemoryCategoriesRepo:
    
    def __init__(self, cats={}):
        self.categories=cats
    
    def get_all(self,):
        return self.categories

    def find_by_name(self,name):
        return self.categories[name]

    def save(self,name,texts):...
