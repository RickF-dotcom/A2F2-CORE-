# A2F2 — ENGINE MASTER
# Controlador operacional principal do ecossistema
# Arquivo: a2f2-engine.py
# Versão: 0.1

from a2f2_masterlink import A2F2MasterLink
from a2f2_savepoint import A2F2_Savepoint
from a2f2_storage import A2F2_Storage

class A2F2Engine:

    def __init__(self):
        self.masterlink = A2F2MasterLink()
        self.storage = A2F2_Storage("a2f2_engine_data")
        self.savepoint = A2F2_Savepoint(self.storage)
        self.state = {
            "executions": 0,
            "registered_sources": [],
            "last_run": None
        }

    # ----------------------------------------
    # REGISTRAR FONTE
    # ----------------------------------------
    def add_source(self, name):
        self.masterlink.registrar_fonte(name)
        self.state["registered_sources"].append(name)

    # ----------------------------------------
    # EXECUTAR PIPELINE COMPLETO
    # ----------------------------------------
    def run(self):
        resultado = self.masterlink.executar()
        self.state["executions"] += 1
        self.state["last_run"] = resultado
        return resultado

    # ----------------------------------------
    # SAVEPOINT
    # ----------------------------------------
    def criar_save(self, tag="auto-save"):
        return self.savepoint.criar(self.state, tag)

    def restaurar_save(self, tag):
        dado = self.savepoint.carregar(tag)
        if "error" in dado:
            return dado
        return self.savepoint.restaurar(self)

    # ----------------------------------------
    # STATUS
    # ----------------------------------------
    def status(self):
        return {
            "state": self.state,
            "masterlink": self.masterlink.status(),
            "savepoints": self.savepoint.listar()
        }

if __name__ == "__main__":
    eng = A2F2Engine()
    print("Engine status inicial:", eng.status())
