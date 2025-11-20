# A²F² — CLI (Command Line Interface)
# Interface simples para interagir com o ecossistema A²F² via terminal
# Arquivo: a2f2-cli.py
# Versão: 0.1

import sys
from a2f2_bootstrap import iniciar_a2f2

def main():
    sistema = iniciar_a2f2()

    print("\n=== A²F² — COMMAND LINE INTERFACE ===")
    print("Comandos disponíveis:")
    print("  add <fonte>        → registrar uma fonte")
    print("  run                → executar pipeline completo")
    print("  status             → exibir status do sistema")
    print("  exit               → sair")

    while True:
        cmd = input("\nA²F² > ").strip().split(" ")

        if cmd[0] == "add":
            if len(cmd) < 2:
                print("Informe o nome da fonte.")
            else:
                fonte = cmd[1]
                sistema.registrar_fonte(fonte)
                print(f"Fonte '{fonte}' adicionada.")

        elif cmd[0] == "run":
            resultado = sistema.executar()
            print("Pipeline executado:")
            print(resultado)

        elif cmd[0] == "status":
            print("STATUS DO SISTEMA:")
            print(sistema.status())

        elif cmd[0] == "exit":
            print("Encerrando CLI...")
            sys.exit(0)

        else:
            print("Comando não reconhecido. Use: add, run, status, exit.")

if __name__ == "__main__":
    main()
