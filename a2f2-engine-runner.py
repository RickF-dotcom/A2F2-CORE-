# A2F2 — Runner Oficial
# Arquivo: a2f2-engine-runner.py
# Versão 0.3

from a2f2_engine_init import A2F2Engine

try:
    from aurion_fehmacou_fehracop_bridge import A2F2_BRIDGE
except:
    A2F2_BRIDGE = None


class A2F2_Runner:
    def __init__(self):
        if A2F2_BRIDGE is None:
            raise RuntimeError("Bridge A2F2 não encontrada.")
        self.bridge = A2F2_BRIDGE()
        self.engine = A2F2Engine(bridge=self.bridge)

    def iniciar(self):
        return self.engine.start()

    def parar(self):
        return self.engine.stop()

    def executar(self, termo):
        return self.engine.executar_fluxo(termo)

    def savepoint(self, tag):
        return self.engine.gerar_savepoint(tag)

    def status(self):
        return self.engine.status()


if __name__ == "__main__":
    runner = A2F2_Runner()
    runner.iniciar()
    print("A2F2 Runner Ativo")
