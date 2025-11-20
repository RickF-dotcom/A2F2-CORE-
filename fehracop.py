# FEHRACOP — Ferramenta de Resiliência, Acompanhamento e Correção Operacional do Protocolo
# Versão 0.1
# Autor: Rick / A²F² – Atena

import time
from typing import Any, Dict, List

class FEHRACOP:
    """
    FEHRACOP: subsistema responsável por:
    - supervisão contínua de módulos
    - detecção e isolamento de falhas
    - política de fallback e veto
    - registro audit trail para decisões críticas
    - orquestração de reinicializações e rollbacks seguros
    """

    def __init__(self):
        self.status_modulos: Dict[str, str] = {}
        self.audit_log: List[Dict[str, Any]] = []
        self.last_check = time.time()

    # --- Supervisão ---
    def registrar_status(self, modulo: str, status: str):
        """Registra o estado atual de um módulo (OK, WARN, FAIL, ISOLADO)."""
        self.status_modulos[modulo] = status
        self._audit(f"Status registrado: {modulo} -> {status}")

    def checar_integridade(self) -> Dict[str, str]:
        """Retorna o mapa atual de status dos módulos."""
        self.last_check = time.time()
        self._audit("Checagem de integridade executada.")
        return dict(self.status_modulos)

    # --- Resposta a falhas ---
    def isolar_modulo(self, modulo: str):
        """Isola um módulo com falha para proteger o sistema."""
        self.status_modulos[modulo] = "ISOLADO"
        self._audit(f"Isolamento executado: {modulo}")

    def reiniciar_modulo(self, modulo: str) -> bool:
        """
        Tenta reiniciar o módulo.
        Retorna True se a tentativa foi disparada (não garante sucesso interno).
        """
        self._audit(f"Tentativa de reinício: {modulo}")
        self.status_modulos[modulo] = "REINICIANDO"
        return True

    def aplicar_rollback(self, modulo: str, versao_alvo: str) -> bool:
        """Registra um pedido de rollback para versão alvo."""
        self._audit(f"Rollback solicitado: {modulo} -> {versao_alvo}")
        self.status_modulos[modulo] = f"ROLLBACK->{versao_alvo}"
        return True

    # --- Política de veto e fallback ---
    def veto_operacao(self, operacao_id: str, motivo: str):
        """Registra um veto que impede execução de operação crítica."""
        self._audit(f"VETO aplicado: {operacao_id} | motivo: {motivo}")
        return {"operacao": operacao_id, "veto": True, "motivo": motivo}

    def fallback_plan(self, operacao_id: str) -> Dict[str, Any]:
        """Gera um plano de fallback simples para uma operação."""
        plano = {"operacao": operacao_id, "plano": "re-rota para subsistema redundante"}
        self._audit(f"Fallback gerado: {operacao_id}")
        return plano

    # --- Auditoria ---
    def _audit(self, mensagem: str):
        """Registra entrada no log de auditoria com timestamp."""
        registro = {"t": time.time(), "msg": mensagem}
        self.audit_log.append(registro)

    def recuperar_audit(self, ultimo_n: int = 50) -> List[Dict[str, Any]]:
        """Retorna as últimas N entradas do audit log (mais recentes primeiro)."""
        return list(reversed(self.audit_log[-ultimo_n:]))

    # --- Utilitários ---
    def resumo(self) -> Dict[str, Any]:
        """Resumo rápido do estado do FEHRACOP."""
        return {
            "modulos_monitorados": len(self.status_modulos),
            "ultima_checagem": self.last_check,
            "entradas_audit": len(self.audit_log),
        }
