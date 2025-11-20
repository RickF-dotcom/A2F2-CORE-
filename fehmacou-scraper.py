# FEHMACOU — Scraper Interno (Simulação)
# Versão: 0.1
# Arquivo: fehmacou-scraper.py

import time
import random

class FEHMACOUScraper:

    def __init__(self, netmap=None, cache=None):
        self.netmap = netmap
        self.cache = cache

    def fetch(self, source_name):
        """
        Simulação de busca externa.
        Caso exista no cache, retorna cache.
        Caso contrário, 'busca' e guarda.
        """
        if self.cache:
            cached = self.cache.get(source_name)
            if cached:
                return {
                    "source": source_name,
                    "cached": True,
                    "data": cached
                }

        source = self.netmap.get_source(source_name) if self.netmap else None
        if not source:
            return {
                "error": "SOURCE_NOT_FOUND",
                "source": source_name
            }

        # Simulando busca (latência + random)
        time.sleep(0.1)
        data = {
            "url": source["url"],
            "timestamp": time.time(),
            "payload": f"DADOS_SIMULADOS_{random.randint(1000,9999)}"
        }

        if self.cache:
            self.cache.set(source_name, data)

        return {
            "source": source_name,
            "cached": False,
            "data": data
        }

    def batch_fetch(self, sources: list):
        results = []
        for s in sources:
            results.append(self.fetch(s))
        return results
