# A2F2 — Módulo de Segurança Interna
# Arquivo: a2f2-security.py
# Versão 0.2

import hashlib
import time

class A2F2_Security:
    def __init__(self):
        self.chaves = {}
        self.log = []

    def gerar_chave(self, identificador):
        momento = str(time.time())
        chave = hashlib.sha256((identificador + momento).encode()).hexdigest()

        self.chaves[identificador] = {
            "chave": chave,
            "timestamp": momento
        }

        self._registrar(f"Chave criada para {identificador}")
        return chave

    def validar_chave(self, identificador, chave):
        registro = self.chaves.get(identificador)
        if not registro:
            return False
        return registro["chave"] == chave

    def revogar_chave(self, identificador):
        if identificador in self.chaves:
            del self.chaves[identificador]
            self._registrar(f"Chave revogada para {identificador}")
            return True
        return False

    def _registrar(self, mensagem):
        self.log.append({
            "timestamp": time.time(),
            "evento": mensagem
        })

    def historico(self):
        return self.log
