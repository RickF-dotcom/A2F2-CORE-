# AURION — Auditoria Suprema
# Núcleo Central
# Arquivo: aurion-core.py
# Versão: 0.1

class AurionCore:

    def __init__(self):
        self.queue = []
        self.audit_log = []
        self.credibility_table = {}   # CAC — Controle Aurion de Credibilidade

    # ---------------------------------------------------
    # RECEBE PACOTES PARA AUDITORIA
    # ---------------------------------------------------
    def enqueue_for_audition(self, block):
        self.queue.append(block)

    # ---------------------------------------------------
    # EXECUTA AUDITORIA SOBRE TODA A FILA
    # ---------------------------------------------------
    def audit_all(self):
        audited = []
        while self.queue:
            block = self.queue.pop(0)
            result = self._audit(block)
            audited.append(result)

        return audited

    # ---------------------------------------------------
    # AUDITORIA INDIVIDUAL
    # ---------------------------------------------------
    def _audit(self, block):
        credibility = self._evaluate_credibility(block)
        source = block.get("origin_url", "UNKNOWN")

        # Registra no CAC
        self.credibility_table[source] = credibility

        # Log
        self.audit_log.append({
            "source": source,
            "credibility": credibility
        })

        # Retorna bloco auditado
        block["credibility"] = credibility
        return block

    # ---------------------------------------------------
    # ANÁLISE DE CREDIBILIDADE (CAC)
    # ---------------------------------------------------
    def _evaluate_credibility(self, block):
        payload = block.get("payload", "")

        if not payload:
            return "0.0 — SEM DADOS"

        length = len(payload)

        if length < 50:
            return "1.0 — BAIXA"
        if 50 <= length < 200:
            return "2.5 — MÉDIA"
        if 200 <= length < 500:
            return "4.0 — ALTA"
        return "5.0 — MÁXIMA"

    # ---------------------------------------------------
    # STATUS AURION
    # ---------------------------------------------------
    def status(self):
        return {
            "queue_length": len(self.queue),
            "credibility_sources": len(self.credibility_table),
            "audit_log_entries": len(self.audit_log)
        }
