# test_import_motor.py
# Testa a importação do núcleo do motor A2F2 com fallback para ajustar sys.path em CI

import sys
import os
import traceback

print("\n=== INÍCIO DO TESTE DO MOTOR A2F2 ===\n")

def try_import():
    try:
        print("Tentando import direto: a2f2_motor")
        import a2f2_motor  # import normal se o módulo estiver no path
        print("Módulo 'a2f2_motor' importado com sucesso.")
        return True
    except Exception:
        print("Import direto falhou. Tentando ajustar sys.path e reimportar...")
        # adiciona o diretório do repositório (pai) ao sys.path para CI / execuções locais
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if repo_root not in sys.path:
            print(f"Adicionando repo_root ao sys.path: {repo_root}")
            sys.path.insert(0, repo_root)
        try:
            import a2f2_motor
            print("Módulo 'a2f2_motor' importado após ajustar sys.path.")
            return True
        except Exception as e:
            print("ERRO ao importar 'a2f2_motor' mesmo após ajustar sys.path:")
            traceback.print_exc()
            return False

if __name__ == "__main__":
    ok = try_import()
    if ok:
        print("\n--- FIM DO TESTE: IMPORT OK ---\n")
    else:
        print("\n--- FIM DO TESTE: IMPORT FALHOU ---\n")
        # retornar código de erro (útil para CI)
        raise SystemExit(1)
