# FEHMACOU — NetMap (Mapeamento de Fontes Externas)
# Versão: 0.1
# Arquivo: fehmacou-netmap.py

class FEHMACOUNetMap:

    def __init__(self):
        self.map = {}

    def register_source(self, name, url, category="generic"):
        """
        Registra uma fonte externa com nome, URL e categoria.
        """
        self.map[name] = {
            "url": url,
            "category": category,
            "status": "registered"
        }
        return self.map[name]

    def get_source(self, name):
        return self.map.get(name, None)

    def list_sources(self):
        return self.map

    def categorize(self, name, category):
        if name in self.map:
            self.map[name]["category"] = category
            return True
        return False

    def remove_source(self, name):
        if name in self.map:
            del self.map[name]
            return True
        return False

    def status(self):
        return {
            "total_sources": len(self.map),
            "categories": list({d["category"] for d in self.map.values()})
        }
