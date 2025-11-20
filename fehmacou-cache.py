# FEHMACOU — Internal Cache System
# Versão: 0.1
# Arquivo: fehmacou-cache.py

import time

class FEHMACOUCache:

    def __init__(self, ttl=3600):
        """
        ttl = tempo de vida dos dados em segundos.
        """
        self.ttl = ttl
        self.cache = {}

    def set(self, key, value):
        """
        Armazena dado com timestamp.
        """
        self.cache[key] = {
            "value": value,
            "timestamp": time.time()
        }
        return True

    def get(self, key):
        """
        Retorna dado se não expirou.
        """
        if key not in self.cache:
            return None

        entry = self.cache[key]
        age = time.time() - entry["timestamp"]

        if age > self.ttl:
            del self.cache[key]
            return None
        
        return entry["value"]

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]
            return True
        return False

    def clear(self):
        self.cache = {}
        return True

    def status(self):
        """
        Retorna status geral do cache.
        """
        return {
            "items": len(self.cache),
            "ttl": self.ttl
        }
