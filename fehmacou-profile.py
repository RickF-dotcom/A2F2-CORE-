# FEHMACOU — Profile Manager
# Versão: 0.1
# Arquivo: fehmacou-profile.py

class FEHMACOUProfile:
    def __init__(self):
        # profiles: { source_name: {credibility, last_seen, tags, metadata} }
        self.profiles = {}

    def create_or_update(self, name, credibility=2.5, tags=None, metadata=None):
        tags = tags or []
        metadata = metadata or {}
        profile = self.profiles.get(name, {
            "credibility": credibility,
            "history": [],
            "tags": tags,
            "metadata": metadata,
            "last_seen": None
        })
        profile["credibility"] = credibility
        profile["tags"] = list(set(profile.get("tags", []) + tags))
        profile["metadata"].update(metadata)
        import time
        profile["last_seen"] = time.time()
        profile["history"].append({
            "timestamp": profile["last_seen"],
            "credibility": credibility
        })
        self.profiles[name] = profile
        return profile

    def get(self, name):
        return self.profiles.get(name)

    def list_all(self):
        return list(self.profiles.keys())

    def remove(self, name):
        if name in self.profiles:
            del self.profiles[name]
            return True
        return False

    def top_n_by_credibility(self, n=10):
        items = sorted(self.profiles.items(), key=lambda kv: kv[1].get("credibility",0), reverse=True)
        return [{ "name": k, **v } for k,v in items[:n]]

    def update_credibility(self, name, new_score, reason=None):
        profile = self.profiles.get(name)
        if not profile:
            return self.create_or_update(name, credibility=new_score)
        profile["credibility"] = new_score
        import time
        profile["last_seen"] = time.time()
        profile["history"].append({
            "timestamp": profile["last_seen"],
            "credibility": new_score,
            "reason": reason
        })
        return profile
