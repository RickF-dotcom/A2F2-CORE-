# A2F2 — DIAGNOSTICS MODULE
# Módulo responsável por testes internos, verificação de integridade
# e diagnóstico de comunicação entre todos os núcleos A²F².
#
# Arquivo: a2f2-diagnostics.py
# Versão: 0.1

from a2f2_engine import A2F2Engine

class A2F2Diagnostics:

    def __init__(self):
        self.engine = A2F2Engine()
        self.reports = []

    # ----------------------------------------------------
    # TESTE 1 — Verifica se todos os módulos respondem
    # ----------------------------------------------------
    def test_integridade_geral(self):
        status = self.engine.status()
        ok = True

        checks = {
            "masterlink": bool(status.get("masterlink")),
            "savepoints": isinstance(status.get("savepoints"), list),
            "estado_engine": isinstance(status.get("state"), dict)
        }

        for key, val in checks.items():
            if not val:
                ok = False

        result = {
            "teste": "integridade_geral",
            "resultado": "OK" if ok else "FALHA",
            "checks": checks
        }
        self.reports.append(result)
        return result

    # ----------------------------------------------------
    # TESTE 2 — Execução simulada de pipeline
    # ----------------------------------------------------
    def test_pipeline(self):
        try:
            self.engine.add_source("fonte_diagnostica")
            run = self.engine.run()

            result = {
                "teste": "execucao_pipeline",
                "resultado": "OK",
                "output": run
            }
        except Exception as e:
            result = {
                "teste": "execucao_pipeline",
                "resultado": "FALHA",
                "erro": str(e)
            }

        self.reports.append(result)
        return result

    # ----------------------------------------------------
    # TESTE 3 — Savepoint
    # ----------------------------------------------------
    def test_savepoint(self):
        try:
            sp = self.engine.criar_save("diagnostico")
            rec = self.engine.restaurar_save("diagnostico")

            result = {
                "teste": "savepoint",
                "resultado": "OK",
                "savepoint": sp,
                "restaurado": rec
            }
        except Exception as e:
            result = {
                "teste": "savepoint",
                "resultado": "FALHA",
                "erro": str(e)
            }

        self.reports.append(result)
        return result

    # ----------------------------------------------------
    # RETORNAR RELATÓRIO FINAL
    # ----------------------------------------------------
    def relatorio(self):
        return self.reports

if __name__ == "__main__":
    diag = A2F2Diagnostics()
    print("Teste 1:", diag.test_integridade_geral())
    print("Teste 2:", diag.test_pipeline())
    print("Teste 3:", diag.test_savepoint())
    print("RELATÓRIO FINAL:", diag.relatorio())
