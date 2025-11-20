# A2F2 — Autenticação Interna
# Arquivo: a2f2-auth.py
# Versão 0.2

import time
import hashlib

class A2F2_Auth:
    def __init__(self):
        self.usuarios = {}
        self.tokens = {}

    def registrar_usuario(self, usuario, senha):
        hash_senha = hashlib.sha256(senha.encode()).hexdigest()
        self.usuarios[usuario] = hash_senha
        return True

    def autenticar(self, usuario, senha):
        if usuario not in self.usuarios:
            return None

        hash_senha = hashlib.sha256(senha.encode()).hexdigest()
        if self.usuarios[usuario] != hash_senha:
            return None

        token = self._gerar_token(usuario)
        self.tokens[token] = {
            "usuario": usuario,
            "timestamp": time.time()
        }
        return token

    def validar_token(self, token):
        return token in self.tokens

    def revogar_token(self, token):
        if token in self.tokens:
            del self.tokens[token]
            return True
        return False

    def _gerar_token(self, usuario):
        base = usuario + str(time.time())
        return hashlib.sha256(base.encode()).hexdigest()
