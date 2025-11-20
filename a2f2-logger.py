# A2F2 — Logger Oficial
# Arquivo: a2f2-logger.py
# Versão 0.2

import time

class A2F2_Logger:
    def __init__(self):
        self.registros = []

    def log(self, mensagem):
        entrada = {
            "timestamp": time.time(),
            "mensagem": mensagem
        }
        self.registros.append(entrada)
        print(f"[A2F2-LOG] {mensagem}")
        return entrada

    def ultimos(self, n=20):
        return self.registros[-n:]

    def todos(self):
        return self.registros
