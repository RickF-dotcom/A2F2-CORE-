# A2F2 — Núcleo Analítico
# Arquivo: a2f2-analyzer.py
# Versão 0.2

import time

class A2F2_Analyzer:
    def __init__(self):
        self.registros = []
        self.ultima_analise = None

    def analisar(self, dados):
        timestamp = time.time()

        resultado = {
            "timestamp": timestamp,
            "entrada": dados,
            "resposta": self._processar(dados)
        }

        self.ultima_analise = resultado
        self.registros.append(resultado)

        return resultado

    def _processar(self, dados):
        if isinstance(dados, str):
            return {"tipo": "texto", "tamanho": len(dados)}
        elif isinstance(dados, list):
            return {"tipo": "lista", "itens": len(dados)}
        elif isinstance(dados, dict):
            return {"tipo": "objeto", "chaves": list(dados.keys())}
        else:
            return {"tipo": "desconhecido", "valor": str(dados)}

    def historico(self):
        return self.registros[-50:]
