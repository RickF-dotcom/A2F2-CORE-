# FEHMACOU — Orchestrator
# Versão: 0.1
# Arquivo: fehmacou-orchestrator.py

class FEHMACOUOrchestrator:

    def __init__(self, router=None):
        self.router = router
        self.log = []

    def run_pipeline(self):
        """
        Executa o pipeline completo:
        - limpa fila anterior
        - percorre todas as fontes registradas
        - executa mineração + limpeza + enriquecimento
        - envia para auditoria
        """
        if not self.router:
            return {"error": "ROUTER_NOT_CONNECTED"}

        results = []

        for source_name in self.router.list_sources():
            res = self.router.execute_full_pipeline(source_name)
            results.append({source_name: res})

        self.log.append({"event": "RUN_PIPELINE", "count": len(results)})
        return results

    def run_single(self, source_name):
        if not self.router:
            return {"error": "ROUTER_NOT_CONNECTED"}

        res = self.router.execute_full_pipeline(source_name)
        self.log.append({"event": "RUN_SINGLE", "source": source_name})
        return res

    def status(self):
        return {
            "router_linked": bool(self.router),
            "log_entries": len(self.log)
        }
