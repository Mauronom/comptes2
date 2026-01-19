class MemoryCategoriesRepo:
    
    def __init__(self, cats={}):
        self.categories=cats
    
    def get_all(self,):
        return self.categories

    def find_by_name(self,name):
        return self.categories[name]

    def save(self,name,texts):
        self.categories[name] = texts

    def delete(self, name):
        if name in self.categories:
            del self.categories[name]
            return True
        return False
