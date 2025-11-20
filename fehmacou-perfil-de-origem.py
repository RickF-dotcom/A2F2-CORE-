# FEHMACOU — Perfil Cognitivo de Origem (PCO)
# Versão: 0.3
# Arquivo: fehmacou-perfil-de-origem.py

import hashlib
import time
import random

class PerfilOrigem:

    def __init__(self):
        self.fontes = {}           # armazena perfis das fontes
        self.historico_eventos = []

    # -----------------------------------------------------------
    # Função 1 — Criar ou atualizar o perfil de uma fonte
    # -----------------------------------------------------------
    def registrar_fonte(self, origem, pacote):
        """
        Cria ou atualiza o perfil de uma origem de dados.
        O perfil é uma 'assinatura comportamental'.
        """

        assinatura = hashlib.sha1(pacote["dados"].encode()).hexdigest()

        if origem not in self.fontes:
            self.fontes[origem] = {
                "assinaturas": [],
                "confiabilidade_media": 0.5,
                "frequencia": 0,
                "ultima_coleta": None,
                "desvios": []
            }

        dados_origem = self.fontes[origem]

        dados_origem["assinaturas"].append(assinatura)
        dados_origem["frequencia"] += 1
        dados_origem["ultima_coleta"] = time.time()

        return dados_origem

    # -----------------------------------------------------------
    # Função 2 — Identificar desvio comportamental
    # -----------------------------------------------------------
    def detectar_desvios(self, origem):
        """
        Mede se a fonte está mudando de comportamento.
        Exemplo: manipulação, mudança editorial, injeção de ruído.
        """
        dados = self.fontes.get(origem)

        if not dados or len(dados["assinaturas"]) < 3:
            return {"desvio_detectado": False, "indice": 0.0}

        ultimo = dados["assinaturas"][-1]
        anterior = dados["assinaturas"][-3]

        distancia = sum(
            1 for a, b in zip(ultimo, anterior) if a != b
        ) / len(ultimo)

        desvio = round(distancia, 3)

        if desvio > 0.35:
            dados["desvios"].append(desvio)
            return {"desvio_detectado": True, "indice": desvio}
        else:
            return {"desvio_detectado": False, "indice": desvio}

    # -----------------------------------------------------------
    # Função 3 — Score de confiabilidade da fonte
    # -----------------------------------------------------------
    def calcular_confiabilidade(self, origem):
        """
        Faz o cálculo final do confiabilidade da fonte para o CAC do AURION.
        """
        dados = self.fontes.get(origem)

        if not dados:
            return 0.5

        base = dados["confiabilidade_media"]
        penalidade = sum(dados["desvios"]) * 0.2

        # impede valores fora do limite
        confiabilidade_final = max(0.0, min(5.0, (base * 5) - penalidade))

        return round(confiabilidade_final, 2)

    # -----------------------------------------------------------
    # Função 4 — Gerar relatório da fonte
    # -----------------------------------------------------------
    def relatorio_fonte(self, origem):
        """
        Devolve um diagnóstico completo da fonte.
        """
        if origem not in self.fontes:
            return {"erro": "Fonte não encontrada"}

        dados = self.fontes[origem]

        return {
            "origem": origem,
            "frequencia": dados["frequencia"],
            "confiabilidade": self.calcular_confiabilidade(origem),
            "desvios": dados["desvios"],
            "assinaturas": len(dados["assinaturas"])
        }
