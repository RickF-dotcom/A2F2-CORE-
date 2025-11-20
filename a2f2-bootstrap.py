# A2F2 — Bootstrap (Inicialização Mestre)
# Arquivo: a2f2-bootstrap.py
# Versão 0.2

from a2f2-engine import A2F2_Engine

class A2F2_Bootstrap:
    def __init__(self):
        self.engine = None
        self.log = []

    def iniciar(self):
        self.engine = A2F2_Engine()
        self._registrar("ENGINE iniciado com sucesso.")
        return {"status": "ok", "mensagem": "A2F2 Engine carregado."}

    def executar(self, comando, *args, **kwargs):
        if not self.engine:
            return {"erro": "ENGINE não inicializado."}
        self._registrar(f"Comando executado: {comando}")
        return self.engine.comando(comando, *args, **kwargs)

    def _registrar(self, mensagem):
        self.log.append(mensagem)

    def historico(self):
        return self.log[-50:]
