# A2F2 — Heartbeat Oficial
# Arquivo: a2f2-engine-heartbeat.py
# Versão 0.3

import time

class A2F2_Heartbeat:
    def __init__(self, engine, intervalo=5):
        self.engine = engine
        self.intervalo = intervalo
        self._ativo = False

    def iniciar(self):
        self._ativo = True
        self._loop()

    def parar(self):
        self._ativo = False

    def _loop(self):
        while self._ativo:
            try:
                self.engine._log("HEARTBEAT: ativo")
            except Exception:
                pass
            time.sleep(self.intervalo)
