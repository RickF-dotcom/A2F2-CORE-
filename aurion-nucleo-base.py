# AURION — Núcleo Base
# Versão: 0.3
# Arquivo: aurion-nucleo-base.py

class AURION:
    def __init__(self):
        self.cac = {}  # Classificação AURION de Credibilidade
        self.historico_avaliacoes = []
        self.modo = "Auditoria_Inteligente"
        self.estado = "Inicializado"

    # -----------------------------------------------------------
    # Função 1 — Receber pacote da FEHMACOU
    # -----------------------------------------------------------
    def receber_pacote(self, pacote):
        pacote["estado_aurion"] = "recebido"
        return pacote

    # -----------------------------------------------------------
    # Função 2 — Avaliação inicial de integridade
    # -----------------------------------------------------------
    def avaliar_integridade(self, pacote):
        conteudo = pacote.get("dados", "")
        tamanho = len(conteudo)

        if tamanho == 0:
            pacote["integridade"] = "vazia"
            pacote["nota_integridade"] = 0.0
        elif tamanho < 20:
            pacote["integridade"] = "fraca"
            pacote["nota_integridade"] = 1.5
        elif tamanho < 60:
            pacote["integridade"] = "média"
            pacote["nota_integridade"] = 3.0
        else:
            pacote["integridade"] = "forte"
            pacote["nota_integridade"] = 4.5

        return pacote

    # -----------------------------------------------------------
    # Função 3 — Auditoria profunda de conteúdo
    # -----------------------------------------------------------
    def auditar_conteudo(self, pacote):
        texto = pacote.get("texto_limpo", "")

        # Simulação de auditoria semântica
        diversidade = len(set(texto.split()))
        densidade = diversidade / (len(texto.split()) + 1)

        nota = round(2.5 + (densidade * 2.5), 2)

        pacote["nota_conteudo"] = nota
        return pacote

    # -----------------------------------------------------------
    # Função 4 — Gerar a nota CAC final
    # -----------------------------------------------------------
    def calcular_cac(self, pacote):
        integridade = pacote.get("nota_integridade", 2.5)
        conteudo = pacote.get("nota_conteudo", 2.5)

        # Média ponderada
        cac = round((integridade * 0.4) + (conteudo * 0.6), 2)

        pacote["cac"] = cac
        return pacote

    # -----------------------------------------------------------
    # Função 5 — Registrar CAC interno da origem
    # -----------------------------------------------------------
    def registrar_origem(self, pacote):
        origem = pacote.get("origem", "desconhecida")
        cac = pacote.get("cac", 2.5)

        self.cac[origem] = cac
        return True

    # -----------------------------------------------------------
    # Função 6 — Emitir relatório da avaliação
    # -----------------------------------------------------------
    def relatorio(self, pacote):
        return {
            "origem": pacote.get("origem", "desconhecida"),
            "integridade": pacote.get("integridade"),
            "nota_integridade": pacote.get("nota_integridade"),
            "nota_conteudo": pacote.get("nota_conteudo"),
            "CAC_final": pacote.get("cac")
        }
