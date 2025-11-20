# A2F2 — Roteador Interno
# Arquivo: a2f2-router.py
# Versão 0.2

class A2F2_Router:
    def __init__(self, engine=None, bridge=None):
        self.engine = engine
        self.bridge = bridge
        self.rotas = {}

    def registrar_rota(self, comando, funcao):
        self.rotas[comando.lower()] = funcao

    def executar(self, comando, *args, **kwargs):
        cmd = comando.lower()
        if cmd not in self.rotas:
            return {"erro": f"Comando '{comando}' não encontrado"}

        try:
            return self.rotas[cmd](*args, **kwargs)
        except Exception as e:
            return {"erro": str(e)}

    def rotas_disponiveis(self):
        return list(self.rotas.keys())
