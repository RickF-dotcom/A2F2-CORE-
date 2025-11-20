# A2F2 — Engine de Ativação & Orquestração
# Versão: 0.4
# Arquivo: a2f2-engine-init.py
# Observação: este módulo inicializa e orquestra o fluxo FEHMACOU ↔ AURION ↔ FEHRACOP ↔ ATHENA
# Espera-se que fehmacou.*, aurion_*, fehracop.*, a2f2-bridge.* estejam disponíveis no mesmo ambiente.

import time
import threading
import json

# Importar componentes centrais (nomes conforme módulos entregues)
try:
    from aurion_fehracop_bridge import A2F2_BRIDGE  # caso Bridge seja modularizado
except Exception:
    # fallback para import de módulos individuais se bridge não existir
    try:
        from aurion_fehmacou_fehracop_bridge import A2F2_BRIDGE
    except Exception:
        # placeholder: o engine assume que A2F2_BRIDGE será injetado ou importado externamente
        A2F2_BRIDGE = None

class A2F2Engine:
    def __init__(self, bridge=None):
        # Se um bridge já existir, usa; senão, tenta instanciar A2F2_BRIDGE importado
        self.bridge = bridge if bridge is not None else (A2F2_BRIDGE() if A2F2_BRIDGE is not None else None)
        self.estado = "inicializado"
        self._heartbeat_interval = 5      # segundos (ajustável)
        self._heartbeat_thread = None
        self._heartbeat_run = False
        self.savepoint = {}
        self.history = []
        self.last_status = {}
        self.lock = threading.RLock()

    # -----------------------------------------------------------
    # Start / Stop Engine
    # -----------------------------------------------------------
    def start(self):
        with self.lock:
            self.estado = "ativo"
            self._start_heartbeat()
            self._log("Engine iniciado")
            return True

    def stop(self):
        with self.lock:
            self.estado = "parando"
            self._stop_heartbeat()
            self._log("Engine parado")
            self.estado = "parado"
            return True

    # -----------------------------------------------------------
    # Heartbeat (monitor simples do sistema)
    # -----------------------------------------------------------
    def _heartbeat_loop(self):
        while self._heartbeat_run:
            with self.lock:
                self.last_status = self._collect_status()
                # registro leve
                self._log("HEARTBEAT: " + json.dumps(self.last_status))
            time.sleep(self._heartbeat_interval)

    def _start_heartbeat(self):
        if not self._heartbeat_run:
            self._heartbeat_run = True
            self._heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
            self._heartbeat_thread.start()

    def _stop_heartbeat(self):
        if self._heartbeat_run:
            self._heartbeat_run = False
            if self._heartbeat_thread is not None:
                self._heartbeat_thread.join(timeout=1)

    # -----------------------------------------------------------
    # Status & Diagnóstico
    # -----------------------------------------------------------
    def _collect_status(self):
        status = {
            "engine_estado": self.estado,
            "timestamp": time.time(),
            "bridge_ok": self.bridge is not None,
            "last_action": self.history[-1]["action"] if self.history else None
        }
        return status

    def status(self):
        with self.lock:
            return self.last_status or self._collect_status()

    # -----------------------------------------------------------
    # Execução de fluxo (single-run)
    # -----------------------------------------------------------
    def executar_fluxo(self, termo_busca):
        if self.bridge is None:
            raise RuntimeError("Bridge A2F2 não inicializada.")
        with self.lock:
            self._log(f"Executando fluxo para termo: {termo_busca}")
            resultado = self.bridge.executar_fluxo(termo_busca)
            registro = {
                "timestamp": time.time(),
                "action": "executar_fluxo",
                "termo": termo_busca,
                "resultado": resultado
            }
            self.history.append(registro)
            return resultado

    # -----------------------------------------------------------
    # Savepoint / Restore
    # -----------------------------------------------------------
    def gerar_savepoint(self, tag=None):
        with self.lock:
            sp = {
                "timestamp": time.time(),
                "tag": tag or f"savepoint_{int(time.time())}",
                "estado_engine": self.estado,
                "history_len": len(self.history),
                "last_status": self._collect_status()
            }
            self.savepoint = sp
            self._log("Savepoint gerado: " + sp["tag"])
            return sp

    def restaurar_savepoint(self):
        with self.lock:
            if not self.savepoint:
                raise RuntimeError("Nenhum savepoint disponível.")
            # restauração leve (reaplica estado)
            self.estado = self.savepoint.get("estado_engine", self.estado)
            self._log("Savepoint restaurado: " + str(self.savepoint.get("tag")))
            return self.savepoint

    # -----------------------------------------------------------
    # Utilitários
    # -----------------------------------------------------------
    def _log(self, msg):
        entry = {"t": time.time(), "msg": str(msg)}
        # manter histórico curto para auditoria local
        self.history.append({"timestamp": entry["t"], "action": "log", "message": entry["msg"]})
        # imprimir leve para debugging (pode ser substituído por logger)
        print(f"[A2F2-ENGINE] {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry['t']))} - {entry['msg']}")

    # -----------------------------------------------------------
    # Interface simples de CLI-like (para testes manuais)
    # -----------------------------------------------------------
    def cli_exec(self, comando, arg=None):
        comando = comando.strip().lower()
        if comando == "start":
            return self.start()
        if comando == "stop":
            return self.stop()
        if comando == "status":
            return self.status()
        if comando == "savepoint":
            return self.gerar_savepoint(tag=arg)
        if comando == "restore":
            return self.restaurar_savepoint()
        if comando == "run" and arg:
            return self.executar_fluxo(arg)
        raise ValueError("Comando desconhecido")

# -----------------------------------------------------------
# Executável de exemplo (se rodar diretamente)
# -----------------------------------------------------------
if __name__ == "__main__":
    # Este bloco é uma demonstração local; adaptar conforme ambiente real.
    engine = A2F2Engine()
    try:
        engine.start()
        # demo: executar um termo de teste
        demo = engine.executar_fluxo("lotofacil padrao")
        engine.gerar_savepoint("demo_inicial")
        time.sleep(1)
        print("Resultado demo:", demo)
    except Exception as e:
        print("Erro engine:", e)
    finally:
        engine.stop()
