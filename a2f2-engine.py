# A2F2 — ENGINE (Mecanismo Operacional Mestre)
# Arquivo: a2f2-engine.py
# Versão 0.2

from a2f2-core import A2F2_Core
from a2f2-router import A2F2_Router
from a2f2-dispatcher import A2F2_Dispatcher

class A2F2_Engine:
    def __init__(self):
        self.core = A2F2_Core()
        self.router = A2F2_Router()
        self.dispatcher = A2F2_Dispatcher(router=self.router)
        self._configurar_rotas()

    def _configurar_rotas(self):
        self.router.registrar_rota("analisar", self.core.analisar)
        self.router.registrar_rota("sync", self.core.sincronizar)
        self.router.registrar_rota("estado", self.core.estado)

    def comando(self, texto, *args, **kwargs):
        return self.dispatcher.despachar(texto, *args, **kwargs)
