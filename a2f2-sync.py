# A2F2 — Módulo de Sincronização Interna
# Arquivo: a2f2-sync.py
# Versão 0.2

import time

class A2F2_Sync:
    def __init__(self):
        self.sincronizado = False
        self.ultima_sync = None
        self.registros = []

    def sincronizar(self, dados=None):
        timestamp = time.time()

        registro = {
            "timestamp": timestamp,
            "dados": dados,
            "status": "sincronizado"
        }

        self.sincronizado = True
        self.ultima_sync = timestamp
        self.registros.append(registro)

        return registro

    def status(self):
        return {
            "sincronizado": self.sincronizado,
            "ultima_sync": self.ultima_sync,
            "registros": self.registros[-10:]
        }

    def historico_completo(self):
        return self.registros
