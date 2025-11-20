# A2F2 — Dispatcher Interno
# Arquivo: a2f2-dispatcher.py
# Versão 0.2

import time

class A2F2_Dispatcher:
    def __init__(self, router=None, logger=None):
        self.router = router
        self.logger = logger
        self.historico = []

    def despachar(self, comando, *args, **kwargs):
        registro = {
            "timestamp": time.time(),
            "comando": comando,
            "args": args,
            "kwargs": kwargs
        }

        self.historico.append(registro)

        if self.logger:
            self.logger.log(f"Dispatcher recebeu comando: {comando}")

        if not self.router:
            return {"erro": "Router não configurado"}

        return self.router.executar(comando, *args, **kwargs)

    def ultimos(self, n=20):
        return self.historico[-n:]
