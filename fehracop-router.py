# FEHRACOP — ROUTER
# Ponte final AURION → FEHRACOP
# Arquivo: fehracop-router.py
# Versão: 0.1

class FEHRACOPRouter:

    def __init__(self, aurion=None, fehracop_orchestrator=None):
        self.aurion = aurion
        self.fehracop_orchestrator = fehracop_orchestrator
        self.log = []

    def transferir_pacotes(self):
        """
        Busca todos os pacotes auditados no Aurion e transfere para o FEHRACOP.
        """
        if not self.aurion or not self.fehracop_orchestrator:
            return {"error": "DEPENDENCIAS_NAO_CONECTADAS"}

        # pegar todos os pacotes auditados até agora
        lista = self.aurion.audit_log.copy()

        if not lista:
            return {"status": "SEM_PACOTES"}

        resultado = self.fehracop_orchestrator.alimentar(lista)

        self.log.append({
            "evento": "transferencia",
            "qtde": len(lista)
        })

        return resultado

    def status(self):
        return {
            "aurion_linked": bool(self.aurion),
            "fehracop_orchestrator_linked": bool(self.fehracop_orchestrator),
            "transferencias": len(self.log)
        }
