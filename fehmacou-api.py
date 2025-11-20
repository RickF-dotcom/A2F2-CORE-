# FEHMACOU — API Simulada
# Versão: 0.1
# Arquivo: fehmacou-api.py

class FEHMACOUAPI:
    def __init__(self, orchestrator=None, router=None, netmap=None, cache=None, scraper=None):
        self.orchestrator = orchestrator
        self.router = router
        self.netmap = netmap
        self.cache = cache
        self.scraper = scraper

    def register_source(self, name, url, credibility=2.5, tags=None, metadata=None):
        if self.orchestrator:
            return self.orchestrator.router.register_source(name, url, credibility, tags, metadata)
        if self.router:
            return self.router.register_source(name, url, credibility, tags, metadata)
        return {"error": "no_router"}

    def list_sources(self):
        if self.netmap:
            return self.netmap.list_sources()
        if self.router:
            return self.router.core.sources
        return {}

    def run_full_pipeline(self):
        if self.orchestrator:
            return self.orchestrator.run_pipeline()
        if self.router:
            mined = self.router.execute_full_pipeline()
            return mined
        return {"error": "no_orchestrator"}

    def fetch_source_now(self, source_name):
        if self.scraper:
            return self.scraper.fetch(source_name)
        if self.router:
            return self.router.execute_single(source_name)
        return {"error": "no_scraper"}

    def status(self):
        return {
            "orchestrator": bool(self.orchestrator),
            "router": bool(self.router),
            "netmap": bool(self.netmap),
            "cache": bool(self.cache),
            "scraper": bool(self.scraper)
        }
