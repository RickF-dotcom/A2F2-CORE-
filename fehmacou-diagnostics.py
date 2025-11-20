# FEHMACOU — Diagnostics
# Versão: 0.1
# Arquivo: fehmacou-diagnostics.py

class FEHMACOUDiagnostics:

    def __init__(self, router=None, orchestrator=None, bridge=None):
        self.router = router
        self.orchestrator = orchestrator
        self.bridge = bridge
        self.report = {}

    def run_diagnostics(self):
        self.report = {
            "sources_registered": self._check_sources(),
            "profiles_status": self._check_profiles(),
            "auditor_queue": self._check_auditor_queue(),
            "bridge_status": self._check_bridge(),
            "integrity_score": self._compute_integrity()
        }
        return self.report

    def _check_sources(self):
        if not self.router:
            return "router_not_connected"
        status = self.router.status()
        return status.get("sources_registered", 0)

    def _check_profiles(self):
        if not self.router:
            return "router_not_connected"
        return self.router.profile.list_all()

    def _check_auditor_queue(self):
        if not self.router:
            return "router_not_connected"
        return self.router.auditor.pending()

    def _check_bridge(self):
        if not self.bridge:
            return "bridge_not_connected"
        return self.bridge.status()

    def _compute_integrity(self):
        score = 100

        if self._check_sources() == 0:
            score -= 20
        
        if isinstance(self._check_profiles(), list) and len(self._check_profiles()) == 0:
            score -= 10
        
        if self._check_auditor_queue() > 50:
            score -= 10

        return max(0, score)

    def get_report(self):
        return self.report
