# FEHRACOP — Runner / Executor
# Versão: 0.1
# Arquivo: fehracop-runner.py

from fehracop_core import FEHRACOPCore
from fehracop_orchestrator import FEHRACOPOrchestrator
from fehracop_router import FEHRACOPRouter

class FEHRACOPRunner:
    def __init__(self, aurion=None):
        self.fehracop = FEHRACOPCore()
        self.orchestrator = FEHRACOPOrchestrator(fehracop=self.fehracop)
        self.router = FEHRACOPRouter(aurion=aurion, fehracop_orchestrator=self.orchestrator)
        self.log = []

    def ingest_from_aurion(self):
        res = self.router.transferir_pacotes()
        self.log.append({"event": "ingest", "result": res})
        return res

    def process_all(self):
        res = self.orchestrator.processar()
        self.log.append({"event": "process", "count": len(res) if isinstance(res, list) else 0})
        return res

    def status(self):
        return {
            "fehracop_status": self.fehracop.status(),
            "orchestrator_log_len": len(self.orchestrator.log),
            "router_log_len": len(self.router.log),
            "last_log": self.log[-5:]
        }

if __name__ == "__main__":
    # Demo rápido (fallback: aurion None → router returns error)
    runner = FEHRACOPRunner(aurion=None)
    print("Status inicial:", runner.status())
    ingest = runner.ingest_from_aurion()
    print("Ingest result:", ingest)
    processed = runner.process_all()
    print("Processed:", processed)
    print("Status final:", runner.status())
