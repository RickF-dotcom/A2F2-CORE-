# FEHMACOU — Runner / Executor
# Versão: 0.1
# Arquivo: fehmacou-runner.py

from fehmacou_orchestrator import FEHMACOUOrchestrator
from fehmacou_netmap import FEHMACOUNetMap
from fehmacou_cache import FEHMACOUCache
from fehmacou_scraper import FEHMACOUScraper
from fehmacou_router import FEHMACOURouter
from fehmacou_auditor_hook import FEHMACOUAuditorHook
from fehmacou_aurion_bridge import FEHMACOUAurionBridge

class FEHMACOURunner:
    def __init__(self):
        self.netmap = FEHMACOUNetMap()
        self.cache = FEHMACOUCache()
        self.scraper = FEHMACOUScraper(netmap=self.netmap, cache=self.cache)
        self.router = FEHMACOURouter()
        # link shared components
        self.router.core = self.router.core
        self.router.miner = self.router.miner
        self.router.profile = self.router.profile
        self.router.auditor = self.router.auditor

        self.orchestrator = FEHMACOUOrchestrator()
        # ensure orchestrator uses same router instance
        self.orchestrator.router = self.router

        self.auditor_hook = self.router.auditor if hasattr(self.router, "auditor") else FEHMACOUAuditorHook()
        self.bridge = FEHMACOUAurionBridge(auditor_hook=self.auditor_hook, aurion_client=None)

        self.log = []

    def register_source(self, name, url, credibility=2.5, tags=None, metadata=None):
        # register in netmap and router
        self.netmap.register_source(name, url)
        return self.orchestrator.router.register_source(name, url, credibility, tags, metadata)

    def run_full(self):
        res = self.orchestrator.run_pipeline()
        self.log.append({"event": "run_full", "result": res})
        return res

    def run_single(self, source_name):
        res = self.orchestrator.run_single(source_name)
        self.log.append({"event": "run_single", "source": source_name, "result": res})
        return res

    def dispatch_to_aurion(self, limit=None):
        dispatched = self.bridge.dispatch_all(limit=limit)
        self.log.append({"event": "dispatch", "count": len(dispatched)})
        return dispatched

    def status(self):
        return {
            "netmap": self.netmap.status(),
            "cache": self.cache.status(),
            "router": self.router.status(),
            "auditor_queue": self.router.auditor.pending() if hasattr(self.router, "auditor") else 0,
            "last_log": self.log[-5:]
        }

if __name__ == "__main__":
    runner = FEHMACOURunner()
    # demo registration
    runner.register_source("exemplo.gov", "https://exemplo.gov/dados", credibility=3.2)
    runner.register_source("noticias.x", "https://noticias.x/feed", credibility=2.1)
    # run pipeline
    pipeline = runner.run_full()
    dispatched = runner.dispatch_to_aurion()
    print("Pipeline:", pipeline)
    print("Dispatched:", dispatched)
    print("Status:", runner.status())
