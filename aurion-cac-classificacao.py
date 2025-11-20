# AURION — CAC (Classificação AURION de Credibilidade)
# Versão 0.3
# Arquivo: aurion-cac-classificacao.py

import time

class AURION_CAC:
    def __init__(self):
        # estrutura interna:
        # { fonte: {score, estrelas, nivel, ultima_atualizacao, historico: []} }
        self.cac = {}

    # -----------------------------------------------------------
    # Função 1 — Converter score 0.0–5.0 em estrelas fracionadas
    # -----------------------------------------------------------
    def _score_para_estrelas(self, score):
        if score < 0: score = 0
        if score > 5: score = 5
        return round(score, 1)

    # -----------------------------------------------------------
    # Função 2 — Categorizar o nível da fonte
    # -----------------------------------------------------------
    def _nivel(self, estrelas):
        if estrelas >= 4.5:
            return "Excelente"
        elif estrelas >= 3.5:
            return "Confiável"
        elif estrelas >= 2.5:
            return "Neutro"
        elif estrelas >= 1.5:
            return "Arriscado"
        else:
            return "Manipulado/Suspeito"

    # -----------------------------------------------------------
    # Função 3 — Registrar/atualizar uma fonte
    # -----------------------------------------------------------
    def classificar_fonte(self, fonte, score, detalhes=None):
        estrelas = self._score_para_estrelas(score)
        nivel = self._nivel(estrelas)

        registro = {
            "fonte": fonte,
            "score": round(score, 2),
            "estrelas": estrelas,
            "nivel": nivel,
            "ultima_atualizacao": time.time(),
            "detalhes": detalhes or {},
        }

        # histórico
        anterior = self.cac.get(fonte)
        if anterior:
            registro.setdefault("historico", anterior.get("historico", []))
            registro["historico"].append(anterior)

        self.cac[fonte] = registro
        return registro

    # -----------------------------------------------------------
    # Função 4 — Obter classificação atual da fonte
    # -----------------------------------------------------------
    def obter(self, fonte):
        return self.cac.get(fonte, None)

    # -----------------------------------------------------------
    # Função 5 — Relatório geral de credibilidade
    # -----------------------------------------------------------
    def relatorio(self):
        return {
            "total_fontes": len(self.cac),
            "fontes": self.cac
        }

    # -----------------------------------------------------------
    # Função 6 — Ordenar fontes por confiabilidade
    # -----------------------------------------------------------
    def ranking(self):
        lista = list(self.cac.values())
        lista.sort(key=lambda x: x["estrelas"], reverse=True)
        return lista

    # -----------------------------------------------------------
    # Função 7 — Expurgo de fontes inválidas ou mortas
    # -----------------------------------------------------------
    def expurgar(self, limite_estrelas=0.5):
        removidos = []
        for fonte, info in list(self.cac.items()):
            if info["estrelas"] <= limite_estrelas:
                removidos.append(fonte)
                del self.cac[fonte]
        return removidos
