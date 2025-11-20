# FEHRACOP — ORCHESTRATOR
# Versão: 0.1
# Arquivo: fehracop-orchestrator.py

class FEHRACOPOrchestrator:

    def __init__(self, fehracop=None):
        self.fehracop = fehracop
        self.log = []

    def alimentar(self, pacotes):
        """
        Alimenta o FEHRACOP com pacotes auditados (já vindos do AURION).
        """
        if not self.fehracop:
            return {"error": "FEHRACOP_NOT_LINKED"}

        resultado = self.fehracop.receber(pacotes)
        self.log.append({"evento": "alimentado", "qtde": resultado.get("received")})
        return resultado

    def processar(self):
        """
        Processa tudo que está na inbox.
        """
        if not self.fehracop:
            return {"error": "FEHRACOP_NOT_LINKED"}

        resultados = self.fehracop.processar_todos()
        self.log.append({"evento": "processado", "qtde": len(resultados)})
        return resultados

    def relatorio(self, n=10):
        """
        Últimos relatórios.
        """
        if not self.fehracop:
            return {"error": "FEHRACOP_NOT_LINKED"}

        return self.fehracop.ultimo_relatorio(n)

    def status(self):
        if not self.fehracop:
            return {"error": "FEHRACOP_NOT_LINKED"}

        return {
            "estado_fehracop": self.fehracop.status(),
            "logs": len(self.log)
        }
