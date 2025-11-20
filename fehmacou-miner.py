# FEHMACOU — MINER
# Versão: 0.1
# Arquivo: fehmacou-miner.py

from fehmacou_core import FEHMACOUCore

class FEHMACOUMiner(FEHMACOUCore):

    def __init__(self):
        super().__init__()
        self.mining_log = []

    # Iniciar mineração completa
    def full_mining_cycle(self):
        results = []

        for src in self.sources:
            raw = self.fetch_raw(src)
            cleaned = self.sanitize(raw)
            results.append(cleaned)
            self.mining_log.append({
                "source": src["name"],
                "result": cleaned
            })

        return results

    # Mineração individual
    def mine_one(self, source_name):
        for src in self.sources:
            if src["name"] == source_name:
                raw = self.fetch_raw(src)
                cleaned = self.sanitize(raw)
                self.mining_log.append({
                    "source": src["name"],
                    "result": cleaned
                })
                return cleaned
        
        return None
