# FEHMACOU — Módulo de Integração com AURION
# Versão: 0.3
# Arquivo: fehmacou-integracao-aurion.py

class IntegracaoAurion:

    def __init__(self):
        self.buffer_envio = []
        self.buffer_retorno = []
        self.status = "Aguardando"
        self.pacotes_enviados = 0
        self.pacotes_recebidos = 0

    # -----------------------------------------------------------
    # Função 1 — Enviar pacote bruto ou lapidado para o AURION
    # -----------------------------------------------------------
    def enviar_para_aurion(self, pacote):
        """
        A FEHMACOU chama isto para enviar dados ao AURION.
        O pacote entra no buffer de envio.
        """
        pacote["status_envio"] = "pendente_aurion"
        self.buffer_envio.append(pacote)
        self.pacotes_enviados += 1
        return True

    # -----------------------------------------------------------
    # Função 2 — Receber avaliação CAC do AURION
    # -----------------------------------------------------------
    def receber_do_aurion(self, retorno):
        """
        Quando o AURION finalizar a auditoria,
        este método recebe a devolução.
        """
        retorno["status_retorno"] = "avaliado_por_aurion"
        self.buffer_retorno.append(retorno)
        self.pacotes_recebidos += 1
        return retorno

    # -----------------------------------------------------------
    # Função 3 — Aplicar decisões do AURION
    # -----------------------------------------------------------
    def aplicar_decisao(self, pacote, fehmacou):
        """
        O AURION pode:
        - aprovar
        - rejeitar
        - solicitar refinamento
        - penalizar fonte
        - atualizar CAC
        """

        origem = pacote.get("origem", "desconhecida")
        nota = pacote.get("cac", 2.5)

        # Atualiza o CAC dentro da FEHMACOU
        fehmacou.registrar_cac(origem, nota)

        # Aplicação da decisão
        if nota < 1.5:
            pacote["acao"] = "descartar"
        elif 1.5 <= nota < 3:
            pacote["acao"] = "refinar"
        else:
            pacote["acao"] = "aprovar"

        return pacote

    # -----------------------------------------------------------
    # Função 4 — Sincronização com o fluxo A2F2
    # -----------------------------------------------------------
    def sincronizar(self):
        """
        Mantém o estado de comunicação limpo.
        Garante fluxo contínuo entre FEHMACOU ↔ AURION.
        """
        if len(self.buffer_envio) > 0:
            self.status = "Enviando"
        elif len(self.buffer_retorno) > 0:
            self.status = "Recebendo"
        else:
            self.status = "Estável"

        return self.status

    # -----------------------------------------------------------
    # Função 5 — Relatório de integração
    # -----------------------------------------------------------
    def relatorio(self):
        return {
            "status": self.status,
            "pendentes_envio": len(self.buffer_envio),
            "pendentes_retorno": len(self.buffer_retorno),
            "enviados": self.pacotes_enviados,
            "recebidos": self.pacotes_recebidos
        }
