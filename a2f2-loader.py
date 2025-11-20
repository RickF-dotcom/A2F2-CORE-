# A2F2 — Unified Loader
# Carrega todo o ecossistema A²F² de forma centralizada
#
# Arquivo: a2f2-loader.py
# Versão: 0.1

from a2f2_bootstrap import iniciar_a2f2
from a2f2_engine import A2F2Engine
from a2f2_diagnostics import A2F2Diagnostics
from a2f2_finalize import A2F2Finalize

class A2F2Loader:

    def __init__(self):
        self.engine = None
        self.diag = None
        self.finalize = None
        self.loaded = False

    # ------------------------------------------
    # CARREGAR SISTEMA COMPLETO
    # ------------------------------------------
    def load(self):
        try:
            self.engine = A2F2Engine()
            self.diag = A2F2Diagnostics()
            self.finalize = A2F2Finalize()
            self.loaded = True

            return {
                "status": "A2F2_LOADED",
                "engine": True,
                "diagnostics": True,
                "finalize": True
            }
        except Exception as e:
            return {"error": "load_failed", "detail": str(e)}

    # ------------------------------------------
    # STATUS
    # ------------------------------------------
    def status(self):
        return {
            "loaded": self.loaded,
            "engine_loaded": self.engine is not None,
            "diagnostics_loaded": self.diag is not None,
            "finalize_loaded": self.finalize is not None
        }

if __name__ == "__main__":
    loader = A2F2Loader()
    print("Carregando A2F2...")
    print(loader.load())
    print("Status:", loader.status())
