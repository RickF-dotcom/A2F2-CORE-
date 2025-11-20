# AURION — FEHMACOU → AURION → FEHRACOP
# INTEGRAÇÃO OPERACIONAL OFICIAL DO A²F²
# Arquivo: aurion-fehmacou-fehracop-bridge.py
# Versão 0.4 — Estável

from fehmacou import FEHMACOU
from aurion_core import AURION_CORE
from aurion_cac_classificacao import AURION_CAC
from fehracop import FEHRACOP

class A2F2_BRIDGE:
    def __init__(self):
        self.fehmacou = FEHMACOU()
        self.aurion = AURION_CORE()
        self.cac = AURION_CAC()
        self.fehracop = FEHRACOP()

    # -----------------------------------------------------------
    # 1 — FEHMACOU minera dados da Internet
    # -----------------------------------------------------------
    def minerar(self, termo):
        dados = self.fehmacou.buscar(termo)
        return {
            "termo": termo,
            "dados_brutos": dados
        }

    # -----------------------------------------------------------
    # 2 — AURION audita cada DADO entregue
    # -----------------------------------------------------------
    def auditar(self, dados_brutos):
        resultados = []

        for item in dados_brutos:
            fonte = item.get("fonte", "DESCONHECIDO")
            qualidade = self.aurion.avaliar(item)
            
            # Classificar no CAC
            self.cac.classificar_fonte(
                fonte=fonte,
                score=qualidade["score"],
                detalhes=qualidade
            )

            resultados.append({
                "fonte": fonte,
                "score": qualidade["score"],
                "nivel": qualidade["nivel"],
                "conteudo": item.get("conteudo", {})
            })

        return resultados

    # -----------------------------------------------------------
    # 3 — FEHRACOP recebe somente os dados aprovados
    # -----------------------------------------------------------
    def enviar_para_fehracop(self, auditoria):
        dados_filtrados = []

        for registro in auditoria:
            if registro["score"] >= 3.5:  # Confiável
                dados_filtrados.append(registro)

        self.fehracop.receber(dados_filtrados)

        return {
            "enviados": len(dados_filtrados),
            "descartados": len(auditoria) - len(dados_filtrados),
            "dados": dados_filtrados
        }

    # -----------------------------------------------------------
    # 4 — Operação completa
    # -----------------------------------------------------------
    def executar_fluxo(self, termo_busca):
        # 1) Mineração
        bruto = self.minerar(termo_busca)

        # 2) Auditoria
        auditoria = self.auditar(bruto["dados_brutos"])

        # 3) Entrega ao FEHRACOP
        resultado = self.enviar_para_fehracop(auditoria)

        return {
            "busca": termo_busca,
            "resultado": resultado,
            "cac_status": self.cac.relatorio()
        }
