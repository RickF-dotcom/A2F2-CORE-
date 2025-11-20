# ============================================================
# A2F2 SÍNTESE — MÓDULO DE EXPRESSÃO FINAL
# Versão 0.1
# Arquivo: a2f2-sintese.py
# Autor: Rick / A²F² — Atena
# ============================================================

from a2f2_core.perspectiva import Perspectiva
from a2f2_core.nucleo_integrado import NucleoIntegrado
from a2f2_core.governanca import Governanca

class A2F2Sintese:
    """
    Responsável por transformar o fluxo interno do A2F2
    em uma resposta final clara, coerente e madura.
    """

    def __init__(self):
        self.perspectiva = Perspectiva()
        self.nucleo = NucleoIntegrado()
        self.governanca = Governanca()

    # ============================================================
    # CAMADA 1 — HARMONIZAÇÃO
    # ============================================================
    def harmonizar(self, fluxo):
        """
        Ajusta o fluxo para coerência cognitiva.
        Remove ruído, desalinhamento e excesso estrutural.
        """
        return self.nucleo.harmonizar(fluxo)

    # ============================================================
    # CAMADA 2 — AJUSTE DE PERSPECTIVA
    # ============================================================
    def aplicar_perspectiva(self, fluxo):
        """
        Alinha o fluxo ao estilo cognitivo da Perspectiva.
        Define tom, ritmo, profundidade e maturidade.
        """
        return self.perspectiva.aplicar(fluxo)

    # ============================================================
    # CAMADA 3 — AFINAÇÃO PELA GOVERNANÇA
    # ============================================================
    def governar(self, fluxo):
        """
        Aplica as regras internas de integridade,
        prioridade, profundidade e coerência moral.
        """
        return self.governanca.refinar(fluxo)

    # ============================================================
    # CAMADA 4 — SÍNTESE FINAL
    # ============================================================
    def sintetizar(self, fluxo):
        """
        Última etapa — produz a resposta final lapidada.
        """
        return {
            "estado": "ok",
            "resposta": fluxo
        }

    # ============================================================
    # CANAL ÚNICO — PROCESSO COMPLETO DE SÍNTESE
    # ============================================================
    def processar_resposta(self, fluxo_interno):
        f1 = self.harmonizar(fluxo_interno)
        f2 = self.aplicar_perspectiva(f1)
        f3 = self.governar(f2)
        return self.sintetizar(f3)
