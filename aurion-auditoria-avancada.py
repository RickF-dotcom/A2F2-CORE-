# AURION — Auditoria Avançada de Fontes (CAC++ / Detecção de Manipulação)
# Versão: 0.3
# Arquivo: aurion-auditoria-avancada.py

import math
import statistics
import hashlib
import time

class AuditoriaAvancada:
    def __init__(self):
        self.cac = {}  # Credibilidade por origem
        self.historico = []
        self.flags = {}  # registros de manipulação/alertas

    # -----------------------------------------------------------
    # Função 1 — Checagem de metadados e consistência temporal
    # -----------------------------------------------------------
    def checar_metadados(self, pacote):
        meta = pacote.get("meta", {})
        resultado = {
            "timestamp_ok": True,
            "autor_ok": True,
            "formato_ok": True,
            "detalhes": {}
        }

        ts = meta.get("timestamp")
        if ts:
            try:
                # verifica timestamp plausível (não futuro distante)
                if ts > time.time() + 3600:
                    resultado["timestamp_ok"] = False
                    resultado["detalhes"]["timestamp"] = "futuro"
            except Exception:
                resultado["timestamp_ok"] = False
                resultado["detalhes"]["timestamp"] = "invalido"
        else:
            resultado["timestamp_ok"] = False
            resultado["detalhes"]["timestamp"] = "ausente"

        if not meta.get("autor"):
            resultado["autor_ok"] = False
            resultado["detalhes"]["autor"] = "ausente"

        # formato básico
        if not isinstance(pacote.get("dados", ""), str):
            resultado["formato_ok"] = False
            resultado["detalhes"]["formato"] = "nao_texto"

        pacote["meta_check"] = resultado
        return pacote

    # -----------------------------------------------------------
    # Função 2 — Heurística de anomalia textual (simples)
    # -----------------------------------------------------------
    def detectar_anomalias_textuais(self, texto):
        tokens = text_tokens = texto.split()
        if len(tokens) == 0:
            return {"anomaly": True, "score": 1.0, "reason": "vazio"}

        uniq = len(set(tokens))
        repeticao_ratio = 1 - (uniq / len(tokens))
        avg_token_len = statistics.mean([len(t) for t in tokens]) if tokens else 0

        # heurística: muita repetição ou tokens muito curtos pode indicar manipulação/ruído
        score = round(min(1.0, (repeticao_ratio * 1.5) + (0.01 * (5 - avg_token_len))), 3)
        anomaly = score > 0.35

        return {"anomaly": anomaly, "score": score, "repeticao_ratio": round(repeticao_ratio,3), "avg_token_len": round(avg_token_len,2)}

    # -----------------------------------------------------------
    # Função 3 — Cross-check rápido entre múltiplos pacotes (coerência)
    # -----------------------------------------------------------
    def cross_check_coerencia(self, pacotes):
        """
        Recebe lista de pacotes (mesmo tema) e calcula coerência entre eles.
        Retorna índice de coerência [0..1], onde 1 = totalmente coerente.
        """
        hashes = []
        for p in pacotes:
            s = p.get("texto_limpo") or p.get("dados","")
            h = hashlib.md5(s.encode()).hexdigest()
            hashes.append(h)

        unique = len(set(hashes))
        total = len(hashes) if hashes else 1
        coerencia = 1 - ((unique - 1) / max(1, total - 1)) if total > 1 else 1.0
        coerencia = max(0.0, min(1.0, coerencia))
        return {"coerencia": round(coerencia,3), "total": total, "unicos": unique}

    # -----------------------------------------------------------
    # Função 4 — Calculo CAC Avançado (ponderações e penalidades)
    # -----------------------------------------------------------
    def calcular_cac_avancado(self, pacote, contexto_pacotes=None):
        """
        Combina:
         - nota_integridade (0-5)
         - nota_conteudo (0-5)
         - metadados (bônus/malus)
         - anomalias textuais (penalidade)
         - coerência com outros pacotes (bônus)
        Retorna CAC no intervalo 0.0 - 5.0
        """
        integridade = pacote.get("nota_integridade", 2.5)
        conteudo = pacote.get("nota_conteudo", 2.5)

        meta = pacote.get("meta_check", {})
        meta_bonus = 0.0
        if meta.get("timestamp_ok") and meta.get("autor_ok"):
            meta_bonus += 0.4
        elif not meta.get("timestamp_ok"):
            meta_bonus -= 0.6

        # anomalia textual
        texto = pacote.get("texto_limpo", pacote.get("dados", ""))
        anom = self.detectar_anomalias_textuais(texto)
        penalty = anom["score"] * 1.8  # penaliza fortemente se anomalia alta

        # coerência com contexto
        coer_bonus = 0.0
        if contexto_pacotes:
            cc = self.cross_check_coerencia(contexto_pacotes)
            coer_bonus += (cc["coerencia"] - 0.5) * 0.8  # ajusta com base na coerência

        raw = (integridade * 0.35) + (conteudo * 0.45) + meta_bonus + coer_bonus - penalty
        cac = max(0.0, min(5.0, round((raw / 5.0) * 5.0, 2)))  # normaliza para 0-5 mantendo escala
        pacote["cac_advance"] = cac
        pacote["anomalia_textual"] = anom
        return pacote

    # -----------------------------------------------------------
    # Função 5 — Registrar e sinalizar manipulações
    # -----------------------------------------------------------
    def registrar_avaliacao(self, pacote):
        origem = pacote.get("origem", "desconhecida")
        cac = pacote.get("cac_advance", pacote.get("cac", 2.5))
        self.cac[origem] = cac
        entry = {
            "timestamp": time.time(),
            "origem": origem,
            "cac": cac,
            "meta": pacote.get("meta_check"),
            "anomalia": pacote.get("anomalia_textual")
        }
        self.historico.append(entry)

        # sinalização: fontes com cac muito baixo e anomalia alta
        if cac < 1.5 and pacote.get("anomalia_textual", {}).get("score",0) > 0.4:
            self.flags.setdefault(origem, []).append({
                "reason": "suspeita_manipulacao",
                "score": pacote["anomalia_textual"]["score"],
                "cac": cac,
                "time": entry["timestamp"]
            })

        return True

    # -----------------------------------------------------------
    # Função 6 — Relatório completo de auditoria
    # -----------------------------------------------------------
    def relatorio_completo(self, pacote):
        return {
            "origem": pacote.get("origem"),
            "nota_integridade": pacote.get("nota_integridade"),
            "nota_conteudo": pacote.get("nota_conteudo"),
            "cac_simple": pacote.get("cac"),
            "cac_advance": pacote.get("cac_advance"),
            "meta_check": pacote.get("meta_check"),
            "anomalia_textual": pacote.get("anomalia_textual"),
            "flags": self.flags.get(pacote.get("origem"), [])
        }

    # -----------------------------------------------------------
    # Função 7 — Endpoint de auditoria (pipeline integrado)
    # -----------------------------------------------------------
    def auditar_pipeline(self, pacote, contexto_pacotes=None):
        """
        Pipeline integrado: receber -> checar meta -> auditar conteudo -> calcular cac avançado -> registrar -> retornar relatório
        """
        pacote = self.receber_pacote(pacote)
        pacote = self.checar_metadados(pacote)
        pacote = self.avaliar_integridade(pacote)
        pacote = self.auditar_conteudo(pacote)
        pacote = self.calcular_cac_avancado(pacote, contexto_pacotes=contexto_pacotes)
        self.registrar_avaliacao(pacote)
        return self.relatorio_completo(pacote)
