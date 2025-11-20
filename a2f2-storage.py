# A2F2 — Módulo de Armazenamento Interno
# Arquivo: a2f2-storage.py
# Versão 0.2

import json
import time
import os

class A2F2_Storage:
    def __init__(self, base="a2f2_data"):
        self.base = base
        if not os.path.exists(self.base):
            os.makedirs(self.base)

    def _arquivo(self, nome):
        return os.path.join(self.base, f"{nome}.json")

    def salvar(self, nome, dados):
        caminho = self._arquivo(nome)
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            return {"erro": str(e)}

    def carregar(self, nome):
        caminho = self._arquivo(nome)
        if not os.path.exists(caminho):
            return None
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {"erro": str(e)}

    def listar(self):
        return [arq for arq in os.listdir(self.base) if arq.endswith(".json")]

    def excluir(self, nome):
        caminho = self._arquivo(nome)
        if os.path.exists(caminho):
            os.remove(caminho)
            return True
        return False
