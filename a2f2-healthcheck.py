# A2F2 — Healthcheck (Verificação de Integridade)
# Arquivo: a2f2-healthcheck.py
# Versão 0.2

import time

class A2F2_Healthcheck:
    def __init__(self, engine=None):
        self.engine = engine
        self.status = "desconhecido"
        self.ultima_verificacao = None
        self.registros = []

    def verificar(self):
        timestamp = time.time()

        if not self.engine:
            resultado = {
                "status": "falha",
                "detalhe": "ENGINE não carregado"
            }
        else:
            resultado = {
                "status": "ok",
                "detalhe": "ENGINE operacional"
            }

        self.status = resultado["status"]
        self.ultima_verificacao = timestamp

        self.registros.append({
            "timestamp": timestamp,
            "resultado": resultado
        })

        return resultado

    def historico(self):
        return self.registros[-20:]

    def estado(self):
        return {
            "status_atual": self.status,
            "ultima_verificacao": self.ultima_verificacao
        }
