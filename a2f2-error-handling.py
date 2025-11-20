# A2F2 — Módulo de Tratamento de Erros
# Arquivo: a2f2-error-handling.py
# Versão 0.2

import time

class A2F2_ErrorHandling:
    def __init__(self, logger=None):
        self.logger = logger
        self.erros = []

    def registrar_erro(self, origem, excecao):
        registro = {
            "timestamp": time.time(),
            "origem": origem,
            "erro": str(excecao)
        }
        self.erros.append(registro)

        if self.logger:
            self.logger.log(f"ERRO em {origem}: {excecao}")

        return registro

    def ultimos(self, n=10):
        return self.erros[-n:]

    def todos(self):
        return self.erros
