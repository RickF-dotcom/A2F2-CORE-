# FEHMACOU → AURION Bridge
# Versão: 0.1
# Arquivo: fehmacou-aurion-bridge.py

from fehmacou_auditor_hook import FEHMACOUAuditorHook

class FEHMACOUAurionBridge:
    def __init__(self, auditor_hook=None, aurion_client=None):
        self.auditor = auditor_hook if auditor_hook is not None else FEHMACOUAuditorHook()
        # aurion_client: objeto que implementa método `auditar_pipeline(pacote, contexto_pacotes=None)`
        self.aurion = aurion_client
        self.history = []
        self.last_dispatch = None

    def set_aurion_client(self, aurion_client):
        self.aurion = aurion_client

    def dispatch_next_to_aurion(self, contexto_pacotes=None):
        pkg = self.auditor.dispatch_next()
        if not pkg:
            return None

        # Normalizar pacote para AURION
        payload = pkg.get("payload", {})
        pacote_para_aurion = {
            "origem": payload.get("source") or payload.get("source_name") or "desconhecida",
            "dados": payload,
            "texto_limpo": payload.get("cleaned") if isinstance(payload.get("cleaned"), str) else str(payload.get("cleaned")),
            "meta": payload.get("meta", {}),
            "status": pkg.get("status", "dispatched")
        }

        resultado = None
        if self.aurion and hasattr(self.aurion, "auditar_pipeline"):
            try:
                resultado = self.aurion.auditar_pipeline(pacote_para_aurion, contexto_pacotes=contexto_pacotes)
            except Exception as e:
                resultado = {"error": str(e)}
        else:
            # fallback: apenas registra o pacote pronto para auditoria manual
            resultado = {"queued_for_audition": pacote_para_aurion}

        registro = {
            "timestamp": __import__("time").time(),
            "pacote_origem": pacote_para_aurion["origem"],
            "resultado": resultado
        }

        self.history.append(registro)
        self.last_dispatch = registro
        return registro

    def dispatch_all(self, contexto_pacotes=None, limit=None):
        dispatched = []
        while True:
            if limit is not None and len(dispatched) >= limit:
                break
            reg = self.dispatch_next_to_aurion(contexto_pacotes=contexto_pacotes)
            if not reg:
                break
            dispatched.append(reg)
        return dispatched

    def status(self):
        return {
            "pending": self.auditor.pending(),
            "last_dispatch": self.last_dispatch,
            "history_len": len(self.history)
        }
