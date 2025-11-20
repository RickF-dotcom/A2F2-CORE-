# A2F2 — Núcleo de Autonomia Assistida
# Arquivo: a2f2-autonomy.py
# Versão 0.2

import time

class A2F2_Autonomy:
    def __init__(self):
        self.estado = "ocioso"
        self.ultima_acao = None
        self.historico = []

    def definir_estado(self, estado):
        self.estado = estado
        self._registrar(f"Estado definido para: {estado}")

    def executar(self, tarefa, dados=None):
        registro = {
            "timestamp": time.time(),
            "tarefa": tarefa,
            "dados": dados
        }
        self.ultima_acao = registro
        self.historico.append(registro)
        return registro

    def obter_estado(self):
        return {
            "estado": self.estado,
            "ultima_acao": self.ultima_acao
        }

    def _registrar(self, mensagem):
        self.historico.append({
            "timestamp": time.time(),
            "evento": mensagem
        })
