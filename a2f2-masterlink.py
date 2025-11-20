# A²F² — MASTERLINK
# Núcleo de ligação unificada entre:
# ATHENA + AURION + FEHMACOU + FEHRACOP
#
# Arquivo: a2f2-masterlink.py
# Versão: 0.1

from aurion_core import AurionCore
from aurion_router import AurionRouter
from fehmacou_intelligence import FEHMACOUIntelligence
from fehmacou_orchestrator import FEHMACOUOrchestrator
from fehracop_core import FEHRACOPCore
from fehracop_orchestrator import FEHRACOPOrchestrator
from fehracop_router import FEHRACOPRouter

class A2F2MasterLink:

    def __init__(self):
        # Instâncias principais
        self.aurion = AurionCore()
        self.fehmacou_intel = FEHMACOUIntelligence()
        self.fehmacou_router = AurionRouter(fehmacou=self.fehmacou_intel,
                                            aurion=self.aurion)
        self.fehmacou_orch = FEHMACOUOrchestrator(router=self.fehmacou_router)

        self.fehracop_core = FEHRACOPCore()
        self.fehracop_orch = FEHRACOPOrchestrator(self.fehracop_core)
        self.fehracop_router = FEHRACOPRouter(self.aurion,
                                              self.fehracop_orch)

        self.system_log = []

    # ————————————————————————————————
    # REGISTRAR FONTE
    # ————————————————————————————————
    def registrar_fonte(self, nome):
        self.fehmacou_router.register_source(nome)
        self.system_log.append({"evento": "fonte_registrada", "nome": nome})

    # ————————————————————————————————
    # EXECUTAR PIPELINE COMPLETO
    # ————————————————————————————————
    def executar(self):
        """
        Roda toda a cadeia:
        FEHMACOU → AURION → FEHRACOP
        """
        processados = self.fehmacou_orch.run_pipeline()
        transfer = self.fehracop_router.transferir_pacotes()
        final = self.fehracop_orch.processar()

        self.system_log.append({
            "evento": "pipeline_completo",
            "processados": processados,
            "transferidos": transfer,
            "finalizados": final
        })

        return {
            "processados": processados,
            "auditoria": transfer,
            "resultado_final": final
        }

    # ————————————————————————————————
    # STATUS
    # ————————————————————————————————
    def status(self):
        return {
            "aurion": self.aurion.status(),
            "fehmacou": self.fehmacou_router.status(),
            "fehracop": self.fehracop_orch.status(),
            "system_log_len": len(self.system_log)
        }

if __name__ == "__main__":
    a2f2 = A2F2MasterLink()
    print("STATUS INICIAL:", a2f2.status())
    a2f2.registrar_fonte("fonte_teste_abc")
    print("EXECUTANDO PIPELINE...")
    resultado = a2f2.executar()
    print("RESULTADO:", resultado)
    print("STATUS FINAL:", a2f2.status())
