# A2F2 — Utilidades Gerais
# Arquivo: a2f2-utils.py
# Versão 0.2

import time
import json
import hashlib

class A2F2_Utils:

    @staticmethod
    def agora():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @staticmethod
    def timestamp():
        return time.time()

    @staticmethod
    def json_limpo(dados):
        try:
            return json.dumps(dados, ensure_ascii=False, indent=2)
        except:
            return str(dados)

    @staticmethod
    def hash_texto(texto):
        if not isinstance(texto, str):
            texto = str(texto)
        return hashlib.sha256(texto.encode("utf-8")).hexdigest()

    @staticmethod
    def validar(dados):
        return dados is not None and dados != "" and dados != {}

    @staticmethod
    def limitar_lista(lista, n=20):
        return lista[-n:] if len(lista) > n else lista
