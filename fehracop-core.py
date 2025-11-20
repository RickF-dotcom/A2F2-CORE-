# FEHRACOP — CORE
# Versão: 0.1
# Arquivo: fehracop-core.py

class FEHRACOPCore:
    def __init__(self):
        self.inbox = []
        self.processed = []
        self.state = "initialized"

    def receber(self, pacotes):
        """
        Recebe lista de pacotes auditados (por AURION) ou pacote único.
        """
        if isinstance(pacotes, dict):
            pacotes = [pacotes]
        for p in pacotes:
            entry = {
                "timestamp": __import__("time").time(),
                "origem": p.get("origem") or p.get("source") or "desconhecida",
                "payload": p
            }
            self.inbox.append(entry)
        return {"received": len(pacotes)}

    def processar_todos(self):
        """
        Processa todos os pacotes da inbox em lote, transformando em outputs utilizáveis.
        """
        resultados = []
        while self.inbox:
            item = self.inbox.pop(0)
            resultado = self._processar_item(item)
            self.processed.append(resultado)
            resultados.append(resultado)
        return resultados

    def _processar_item(self, item):
        payload = item.get("payload", {})
        # transformação básica: extrair campos relevantes e adicionar meta
        processed = {
            "origem": item.get("origem"),
            "conteudo": payload.get("dados") or payload.get("conteudo") or payload,
            "credibilidade": payload.get("credibility") or payload.get("credibility_hint") or "ND",
            "process_timestamp": __import__("time").time()
        }
        return processed

    def ultimo_relatorio(self, n=10):
        return self.processed[-n:]

    def status(self):
        return {
            "inbox_len": len(self.inbox),
            "processed_len": len(self.processed),
            "state": self.state
        }
