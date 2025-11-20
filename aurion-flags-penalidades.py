# AURION — Sistema de Flags & Penalidades
# Versão: 0.3
# Arquivo: aurion-flags-penalidades.py

import time

class FlagsPenalidades:
    def __init__(self):
        # estrutura: { origem: [ {time, reason, score, details} ] }
        self.flags = {}
        # penalidades: { origem: {level, bloqueado, motivo, timestamp} }
        self.penalidades = {}
        # blacklist simples
        self.blacklist = set()
        # thresholds configuráveis
        self.threshold_flag_manip = 0.4
        self.threshold_penal_baixa = 1.2
        self.threshold_block = 0.8

    # -----------------------------------------------------------
    # Função 1 — Adicionar flag (sinalizar manipulação/suspeita)
    # -----------------------------------------------------------
    def adicionar_flag(self, origem, reason, score, details=None):
        registro = {
            "time": time.time(),
            "reason": reason,
            "score": float(score),
            "details": details or {}
        }
        self.flags.setdefault(origem, []).append(registro)

        # checar se acumulo de flags exige ação
        self._avaliar_acoes(origem)
        return registro

    # -----------------------------------------------------------
    # Função 2 — Avaliar ações a partir de flags acumuladas
    # -----------------------------------------------------------
    def _avaliar_acoes(self, origem):
        eventos = self.flags.get(origem, [])
        if not eventos:
            return None

        # média de score recente (últimos 5)
        recentes = eventos[-5:]
        avg_score = sum(e["score"] for e in recentes) / len(recentes)

        # se média alta de suspeita, aplicar penalidade leve
        if avg_score >= self.threshold_flag_manip and avg_score < self.threshold_penal_baixa:
            self.aplicar_penalidade(origem, level="leve", motivo="suspeita_acumulada", score=avg_score)
        # se média muito alta, aplicar penalidade severa ou bloqueio
        elif avg_score >= self.threshold_penal_baixa:
            self.aplicar_penalidade(origem, level="severa", motivo="manipulacao_confirmada", score=avg_score)
            if avg_score >= self.threshold_block:
                self.bloquear_origem(origem, motivo="bloqueio_por_risco_alto", score=avg_score)

        return {"avg_score": avg_score}

    # -----------------------------------------------------------
    # Função 3 — Aplicar penalidade programática
    # -----------------------------------------------------------
    def aplicar_penalidade(self, origem, level="leve", motivo=None, score=0.0):
        entry = {
            "level": level,
            "bloqueado": False,
            "motivo": motivo or "penalidade_aplicada",
            "timestamp": time.time(),
            "score": float(score)
        }
        # acumula penalidades (última prevalece em detalhes)
        self.penalidades[origem] = entry
        return entry

    # -----------------------------------------------------------
    # Função 4 — Bloquear / colocar em blacklist
    # -----------------------------------------------------------
    def bloquear_origem(self, origem, motivo=None, score=0.0):
        entry = {
            "level": "bloqueado",
            "bloqueado": True,
            "motivo": motivo or "bloqueio_manual",
            "timestamp": time.time(),
            "score": float(score)
        }
        self.penalidades[origem] = entry
        self.blacklist.add(origem)
        return entry

    # -----------------------------------------------------------
    # Função 5 — Remover penalidade / reabilitar origem
    # -----------------------------------------------------------
    def reabilitar_origem(self, origem, motivo_reabilitacao="reanalise_positiva"):
        if origem in self.blacklist:
            self.blacklist.remove(origem)
        self.penalidades[origem] = {
            "level": "reabilitado",
            "bloqueado": False,
            "motivo": motivo_reabilitacao,
            "timestamp": time.time(),
            "score": 0.0
        }
        return self.penalidades[origem]

    # -----------------------------------------------------------
    # Função 6 — Relatório de flags e penalidades por origem
    # -----------------------------------------------------------
    def relatorio_origem(self, origem):
        return {
            "origem": origem,
            "flags": self.flags.get(origem, []),
            "penalidade": self.penalidades.get(origem, None),
            "blacklisted": origem in self.blacklist
        }

    # -----------------------------------------------------------
    # Função 7 — Relatório sumarizado (todas as origens)
    # -----------------------------------------------------------
    def relatorio_geral(self):
        resumo = {}
        for origem in set(list(self.flags.keys()) + list(self.penalidades.keys())):
            resumo[origem] = {
                "flags_count": len(self.flags.get(origem, [])),
                "penalidade": self.penalidades.get(origem),
                "blacklisted": origem in self.blacklist
            }
        return resumo

    # -----------------------------------------------------------
    # Função 8 — Ajuste de thresholds (autonomia controlada)
    # -----------------------------------------------------------
    def ajustar_thresholds(self, flag_manip=None, penal_baixa=None, block=None):
        if flag_manip is not None:
            self.threshold_flag_manip = float(flag_manip)
        if penal_baixa is not None:
            self.threshold_penal_baixa = float(penal_baixa)
        if block is not None:
            self.threshold_block = float(block)
        return {
            "threshold_flag_manip": self.threshold_flag_manip,
            "threshold_penal_baixa": self.threshold_penal_baixa,
            "threshold_block": self.threshold_block
      }
