# AURION — CAC Engine (Motor de Classificação AURION de Credibilidade)
# Versão: 0.3
# Arquivo: aurion-cac-engine.py

import time
import statistics

class CAEngine:

    def __init__(self):
        self.mapa_global = {}   # { origem: {historico_cac, media, tendencia} }
        self.registros = []     # histórico completo
        self.tendencias = {}    # tendencia cognitiva por origem
        self.limite_baixa_confianca = 1.5
        self.limite_media_confianca = 3.0

    # -----------------------------------------------------------
    # Função 1 — Consolidar CAC
    # -----------------------------------------------------------
    def consolidar(self, pacote):
        origem = pacote.get("origem", "desconhecida")
        cac = pacote.get("cac_advance", pacote.get("cac", 2.5))
        ts = time.time()

        if origem not in self.mapa_global:
            self.mapa_global[origem] = {
                "historico": [],
                "media": 0.0,
                "tendencia": "estavel"
            }

        dados = self.mapa_global[origem]
        dados["historico"].append(cac)

        # atualizar média
        dados["media"] = round(statistics.mean(dados["historico"]), 2)

        # detectar tendência
        if len(dados["historico"]) >= 3:
            ultimos = dados["historico"][-3:]
            if ultimos[2] > ultimos[1] > ultimos[0]:
                dados["tendencia"] = "ascendente"
            elif ultimos[2] < ultimos[1] < ultimos[0]:
                dados["tendencia"] = "descendente"
            else:
                dados["tendencia"] = "estavel"

        # salvar registro geral
        self.registros.append({
            "origem": origem,
            "timestamp": ts,
            "cac": cac,
            "media": dados["media"],
            "tendencia": dados["tendencia"]
        })

        return {
            "origem": origem,
            "cac": cac,
            "media": dados["media"],
            "tendencia": dados["tendencia"]
        }

    # -----------------------------------------------------------
    # Função 2 — Classificação final da origem
    # -----------------------------------------------------------
    def classificar(self, origem):
        if origem not in self.mapa_global:
            return {"origem": origem, "classe": "desconhecida"}

        media = self.mapa_global[origem]["media"]

        if media < self.limite_baixa_confianca:
            classe = "baixa_confiabilidade"
        elif media < self.limite_media_confianca:
            classe = "confiabilidade_moderada"
        else:
            classe = "alta_confiabilidade"

        return {"origem": origem, "classe": classe, "media": media}

    # -----------------------------------------------------------
    # Função 3 — Gerar curva de confiabilidade
    # -----------------------------------------------------------
    def curva_confiabilidade(self, origem):
        if origem not in self.mapa_global:
            return {"erro": "origem_nao_encontrada"}

        h = self.mapa_global[origem]["historico"]

        curva = []
        acumulado = 0

        for i, v in enumerate(h):
            acumulado += v
            curva.append(round(acumulado / (i+1), 3))

        return {
            "origem": origem,
            "curva": curva,
            "media_final": self.mapa_global[origem]["media"]
        }

    # -----------------------------------------------------------
    # Função 4 — Avaliação final da fonte
    # -----------------------------------------------------------
    def avaliacao_final(self, origem):
        dados = self.classificar(origem)
        curva = self.curva_confiabilidade(origem)

        return {
            "origem": origem,
            "classe": dados["classe"],
            "media": dados["media"],
            "curva": curva["curva"],
            "tendencia": self.mapa_global[origem]["tendencia"]
        }

    # -----------------------------------------------------------
    # Função 5 — Relatório geral de todas as fontes
    # -----------------------------------------------------------
    def relatorio_geral(self):
        saida = {}
        for origem, dados in self.mapa_global.items():
            saida[origem] = {
                "media": dados["media"],
                "tendencia": dados["tendencia"],
                "avaliacao": self.classificar(origem)["classe"]
            }
        return saida
