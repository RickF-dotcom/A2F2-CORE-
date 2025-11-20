# A²F² — BOOTSTRAP
# Responsável por iniciar todo o ecossistema A²F²
# Arquivo: a2f2-bootstrap.py
# Versão: 0.1

from a2f2_masterlink import A2F2MasterLink

def iniciar_a2f2():
    sistema = A2F2MasterLink()
    return sistema

if __name__ == "__main__":
    sistema = iniciar_a2f2()
    print("A²F² BOOTSTRAP INICIALIZADO")
    print(sistema.status())
