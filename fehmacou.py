# FEHMACOU — Ferramenta Especial Híbrida de Mineração, Análise, Correção e Operação Universal
# Versão 0.1
# Autor: Rick / A²F² – Atena

class FEHMACOU:
    """
    Núcleo operacional responsável por:
    - varredura de padrões
    - mineração contextual
    - análise fina de dados
    - correção automática
    - saneamento estrutural de módulos
    - suporte à inteligência operacional e estratégica
    """

    def __init__(self):
        self.registros = []
        self.alertas = []
        self.estado = "OK"

    def registrar(self, mensagem):
        """Registra eventos relevantes."""
        self.registros.append(mensagem)

    def alertar(self, mensagem):
        """Cria alertas internos no sistema."""
        self.alertas.append(mensagem)

    def varrer(self, dados):
        """Realiza varredura e identificação de padrões."""
        padroes = {
            "nulos": sum(1 for d in dados if d is None),
            "strings": sum(1 for d in dados if isinstance(d, str)),
            "numeros": sum(1 for d in dados if isinstance(d, (int, float)))
        }
        self.registrar(f"Varredura concluída: {padroes}")
        return padroes

    def corrigir(self, dados):
        """Corrige pequenos erros estruturais automaticamente."""
        corrigido = []
        for d in dados:
            if d is None:
                corrigido.append(0)
            elif isinstance(d, str) and d.strip() == "":
                corrigido.append("vazio")
            else:
                corrigido.append(d)
        self.registrar("Correção automática executada.")
        return corrigido

    def otimizador(self, dados):
        """Otimiza dados para uso no protocolo A²F²."""
        if not dados:
            self.alertar("Tentativa de otimização sem dados.")
            return []

        media = sum(x for x in dados if isinstance(x, (int, float))) / max(
            1, sum(1 for x in dados if isinstance(x, (int, float)))
        )
        self.registrar(f"Média calculada: {media}")

        normalizado = [(x / media) if isinstance(x, (int, float)) else x for x in dados]
        self.registrar("Otimização concluída.")
        return normalizado
