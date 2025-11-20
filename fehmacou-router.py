# FEHMACOU — Router
# Versão: 0.1
# Arquivo: fehmacou-router.py

from fehmacou_core import FEHMACOUCore
from fehmacou_miner import FEHMACOUMiner
from fehmacou_profile import FEHMACOUProfile
from fehmacou_auditor_hook import FEHMACOUAuditorHook

class FEHMACOURouter:

    def __init__(self):
        self.core = FEHMACOUCore()
        self.miner = FEHMACOUMiner()
        self.profile = FEHMACOUProfile()
        self.auditor = FEHMACOUAuditorHook()

    # Registrar fonte e atualizar perfil AO MESMO TEMPO
    def register_source(self, name, url, credibility=2.5, tags=None, metadata=None):
        self.core.register_source(name, url, credibility)
        return self.profile.create_or_update(
            name,
            credibility=credibility,
            tags=tags,
            metadata=metadata
        )

    # Rodar mineração completa + enviar tudo para AURION
    def execute_full_pipeline(self):
        mined = self.miner.full_mining_cycle()
        outputs = []

        for item in mined:
            package = self.auditor.enqueue_for_audition(item)
            outputs.append(package)

        return {
            "mined": mined,
            "queued_for_aurion": outputs
        }

    # Rodar de uma fonte específica
    def execute_single(self, name):
        result = self.miner.mine_one(name)
        if not result:
            return None
        return self.auditor.enqueue_for_audition(result)

    # Status atual
    def status(self):
        return {
            "sources_registered": len(self.core.sources),
            "pending_audition": self.auditor.pending(),
            "profiles": self.profile.list_all()
        }
