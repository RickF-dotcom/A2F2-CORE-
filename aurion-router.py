# AURION — Router
# Coordena a ponte entre FEHMACOU → AURION
# Arquivo: aurion-router.py
# Versão: 0.1

class AurionRouter:

    def __init__(self, fehmacou=None, aurion=None):
        self.fehmacou = fehmacou
        self.aurion = aurion
        self.sources = []

    # Registro de novas fontes
    def register_source(self, source_name):
        self.sources.append(source_name)

    def list_sources(self):
        return self.sources

    # Pipeline completo
    def execute_full_pipeline(self, source_name):
        """
        FEHMACOU → mineração/limpeza/enriquecimento/validação
        AURION → auditoria/credibilidade
        """
        if not self.fehmacou or not self.aurion:
            return {"error": "DEPENDENCIES_NOT_LINKED"}

        processed = self.fehmacou.process(source_name)
        self.aurion.enqueue_for_audition(processed)
        audited = self.aurion.audit_all()

        return {
            "processed": processed,
            "audited": audited
        }

    # Status do Router
    def status(self):
        return {
            "sources": self.sources,
            "fehmacou_linked": bool(self.fehmacou),
            "aurion_linked": bool(self.aurion)
      }
