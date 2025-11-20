# A2F2 — Núcleo Central (CORE)
# Arquivo: a2f2-core.py
# Versão 0.2

from a2f2-memory import A2F2_Memory
from a2f2-analyzer import A2F2_Analyzer
from a2f2-sync import A2F2_Sync
from a2f2-autonomy import A2F2_Autonomy

class A2F2_Core:
    def __init__(self):
        self.memory = A2F2_Memory()
        self.analyzer = A2F2_Analyzer()
        self.sync = A2F2_Sync()
        self.autonomy = A2F2_Autonomy()

    def registrar_evento(self, chave, valor):
        self.memory.salvar_curta(chave, valor)

    def analisar(self, dados):
        resultado = self.analyzer.analisar(dados)
        self.registrar_evento("ultima_analise", resultado)
        return resultado

    def sincronizar(self):
        estado = {
            "memoria_curta": self.memory.memoria_curta,
            "memoria_longa": self.memory.memoria_longa
        }
        return self.sync.sincronizar(estado)

    def estado(self):
        return {
            "memory": self.memory.historico(),
            "ultima_analise": self.analyzer.ultima_analise,
            "sync": self.sync.status(),
            "autonomy": self.autonomy.obter_estado()
        }
