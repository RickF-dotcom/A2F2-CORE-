# AURION — Análise Profunda de Coerência
# Versão: 0.3
# Arquivo: aurion-analise-profunda.py

import re
import statistics
from difflib import SequenceMatcher

class AnaliseProfundaAURION:
    def __init__(self):
        self.historico = []
    
    # -----------------------------------------------------------
    # Função 1 — Similaridade estrutural
    # -----------------------------------------------------------
    def similaridade(self, a, b):
        """
        Mede similaridade entre dois textos ou conteúdos.
        """
        ratio = SequenceMatcher(None, str(a), str(b)).ratio()
        return round(ratio, 4)

    # -----------------------------------------------------------
    # Função 2 — Detecção de contradições simples
    # -----------------------------------------------------------
    def detectar_contradicacoes(self, texto):
        """
        Procura padrões básicos de contradição no texto.
        """
        padroes = [
            (r"\b(nunca)\b.*\b(mas)\b", "Possível contradição detectada"),
            (r"\b(impossível)\b.*\b(porém)\b", "Afirmação absoluta seguida de oposição"),
            (r"\b(garantido)\b.*\b(não é bem assim)\b", "Garantia revertida depois"),
        ]
        alertas = []
        for regex, msg in padroes:
            if re.search(regex, texto, flags=re.IGNORECASE):
                alertas.append(msg)
        return alertas

    # -----------------------------------------------------------
    # Função 3 — Detecção de manipulação semântica
    # -----------------------------------------------------------
    def detectar_manipulacao(self, texto):
        """
        Identifica sinais de exagero retórico, distorções ou indução.
        """
        gatilhos = [
            "100% garantido",
            "nunca falha",
            "verdade absoluta",
            "todos sabem",
            "ninguém discorda",
        ]
        alertas = []
        for gatilho in gatilhos:
            if gatilho.lower() in texto.lower():
                alertas.append(f"Possível manipulação: '{gatilho}'")
        return alertas

    # -----------------------------------------------------------
    # Função 4 — Coerência lógica básica
    # -----------------------------------------------------------
    def coerencia_logica(self, registro):
        """
        Recebe um dict do FEHMACOU e analisa estrutura e coerência.
        """
        coerencia = {
            "dados_vazios": registro.get("dados") in ["", None],
            "origem_presente": "origem" in registro,
            "hash_existente": "hash" in registro,
            "status_ok": registro.get("status") == "aprovado"
        }
        coerencia["coerencia_geral"] = sum([
            0 if coerencia["dados_vazios"] else 1,
            1 if coerencia["origem_presente"] else 0,
            1 if coerencia["hash_existente"] else 0,
            1 if coerencia["status_ok"] else 0
        ]) / 4
        return coerencia

    # -----------------------------------------------------------
    # Função 5 — Registro no histórico A²F²
    # -----------------------------------------------------------
    def registrar(self, pacote, resultado):
        self.historico.append({
            "pacote": pacote,
            "resultado": resultado
        })
        return True

    # -----------------------------------------------------------
    # Função 6 — Relatório avançado
    # -----------------------------------------------------------
    def relatorio_avancado(self):
        return {
            "entradas_analisadas": len(self.historico),
            "ultimos_5_registros": self.historico[-5:]
        }
