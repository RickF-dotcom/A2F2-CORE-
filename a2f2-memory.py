# A2F2 — Memória Base
# Arquivo: a2f2-memory.py
# Versão 0.2

class A2F2_Memory:
    def __init__(self):
        self.memoria_curta = {}
        self.memoria_longa = {}
        self.registros = []

    def salvar_curta(self, chave, valor):
        self.memoria_curta[chave] = valor
        self.registros.append(f"[curta] {chave} -> salvo")

    def salvar_longa(self, chave, valor):
        self.memoria_longa[chave] = valor
        self.registros.append(f"[longa] {chave} -> salvo")

    def obter(self, chave):
        if chave in self.memoria_curta:
            return self.memoria_curta[chave]
        if chave in self.memoria_longa:
            return self.memoria_longa[chave]
        return None

    def limpar_curta(self):
        self.memoria_curta = {}
        self.registros.append("[curta] limpa")

    def historico(self):
        return self.registros[-50:]
