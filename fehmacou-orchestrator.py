# FEHMACOU — Orchestrator
# Versão: 0.1
# Arquivo: fehmacou-orchestrator.py

from fehmacou_router import FEHMACOURouter

class FEHMACOUOrchestrator:

    def __init__(self):
        self.router = FEHMACOURouter()
        self.log = []

    # Registrar múltiplas fontes de forma agrupada
    def bulk_register(self, sources):
        responses = []
        for src in sources:
            name = src.get("name")
            url = src.get("url")
            cred = src.get("credibility", 2.5)
            tags = src.get("tags", [])
            meta = src.get("metadata", {})

            res = self.router.register_source(
                name=name,
                url=url,
                credibility=cred,
                tags=tags,
                metadata=meta
            )
            responses.append(res)

        return responses

    # Pipeline completo FEHMACOU → AURION
    def run_pipeline(self):
        report = self.router.execute_full_pipeline()
        self._log("PIPELINE_COMPLETE", report)
        return report

    # Pipeline parcial (fonte específica)
    def run_single(self, source_name):
        report = self.router.execute_single(source_name)
        self._log("PIPELINE_SINGLE", report)
        return report

    # Status geral
    def status(self):
        base = self.router.status()
        base["log_entries"] = len(self.log)
        return base

    # Registrar evento interno
    def _log(self, event, payload):
        entry = {
            "event": event,
            "payload": payload
        }
        self.log.append(entry)
        return entry
