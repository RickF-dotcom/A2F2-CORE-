# ============================================================
# A2F2 ENGINE — MOTOR PRINCIPAL DE EXECUÇÃO
# Versão 0.1
# Arquivo: a2f2-engine.py
# Autor: Rick / A²F² — Atena
# ============================================================

from a2f2_core.contexto_avaliativo import ContextoAvaliativo
from a2f2_core.inteligencia_estrategica import InteligenciaEstrategica
from a2f2_core.perspectiva import Perspectiva
from a2f2_core.nucleo_integrado import NucleoIntegrado
from a2f2_core.governanca import Governanca

class A2F2Engine:
    """
    MOTOR PRINCIPAL DO SISTEMA A2F2.
    Faz a ponte entre pensar → decidir → executar.
    """

    def __init__(self):
        self.contexto = ContextoAvaliativo()
        self.estrategia = InteligenciaEstrategica()
        self.perspectiva = Perspectiva()
        self.nucleo = NucleoIntegrado()
        self.governanca = Governanca()

    # ============================================================
    # ETAPA 1 — INTERPRETAR
    # ============================================================
    def interpretar(self, entrada):
        leitura = self.contexto.avaliar(entrada)
        return leitura

    # ============================================================
    # ETAPA 2 — ESTRATEGIZAR
    # ============================================================
    def estrategizar(self, leitura):
        plano = self.estrategia.planejar(leitura)
        return plano

    # ============================================================
    # ETAPA 3 — DIRECIONAR
    # ============================================================
    def direcionar(self, plano):
        direcao = self.governanca.definir_direcao(plano)
        return direcao

    # ============================================================
    # ETAPA 4 — INTEGRAR
    # ============================================================
    def integrar(self, direcao):
        fluxo = self.nucleo.integrar(direcao)
        return fluxo

    # ============================================================
    # ETAPA 5 — EXECUTAR
    # ============================================================
    def executar(self, fluxo):
        """
        Aqui será implementado o executor real quando o sistema
        estiver rodando em ambiente externo (Render, VPS, etc.).
        """
        return {
            "estado": "executado",
            "fluxo_processado": fluxo
        }

    # ============================================================
    # CANAL ÚNICO — USAR O SISTEMA COMPLETO
    # ============================================================
    def processar(self, entrada):
        leitura = self.interpretar(entrada)
        plano = self.estrategizar(leitura)
        direcao = self.direcionar(plano)
        fluxo = self.integrar(direcao)
        return self.executar(fluxo)
