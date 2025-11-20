# A2F2 — Diagnósticos Internos
# Arquivo: a2f2-diagnostics.py
# Versão 0.2

import time

class A2F2_Diagnostics:
    def __init__(self, engine):
        self.engine = engine

    def ping(self):
        return {
            "timestamp": time.time(),
            "engine_estado": self.engine.estado,
            "bridge_ok": self.engine.bridge is not None,
            "ultimo_status": self.engine.last_status
        }

    def historico(self, limite=20):
        return self.engine.history[-limite:]

    def detalhes_engine(self):
        return {
            "estado": self.engine.estado,
            "heartbeat_interval": self.engine._heartbeat_interval,
            "savepoint": self.engine.savepoint,
            "history_len": len(self.engine.history)
        }
