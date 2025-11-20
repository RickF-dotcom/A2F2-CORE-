# A2F2 — Savepoint Manager
# Arquivo: a2f2-savepoint.py
# Versão: 0.1

import time
import json
from a2f2_storage import A2F2_Storage

class A2F2_Savepoint:
    def __init__(self, storage=None, namespace="a2f2_savepoints"):
        self.storage = storage if storage is not None else A2F2_Storage(base=namespace)
        self.current = None

    def criar(self, engine_state, tag=None):
        ts = int(time.time())
        meta_tag = tag or f"savepoint_{ts}"
        payload = {
            "tag": meta_tag,
            "timestamp": ts,
            "engine_state": engine_state
        }
        # salvar em arquivo com nome da tag
        ok = self.storage.salvar(meta_tag, payload)
        if ok is True:
            self.current = payload
            return payload
        return {"error": "save_failed", "detail": ok}

    def listar(self):
        arquivos = self.storage.listar()
        # remover sufixo .json
        return [a[:-5] if a.endswith(".json") else a for a in arquivos]

    def carregar(self, tag):
        dado = self.storage.carregar(tag)
        if isinstance(dado, dict) and "error" in dado:
            return dado
        self.current = dado
        return dado

    def restaurar(self, engine):
        """
        Restaura o engine a partir do savepoint atual (ou carrega último se None).
        Retorna o estado restaurado.
        """
        if not self.current:
            # tenta carregar o último save (por timestamp)
            arquivos = self.listar()
            if not arquivos:
                return {"error": "no_savepoints"}
            # carregar todos e escolher o mais recente
            latest = None
            latest_ts = 0
            for tag in arquivos:
                sp = self.storage.carregar(tag)
                if not sp or "timestamp" not in sp:
                    continue
                if sp["timestamp"] > latest_ts:
                    latest_ts = sp["timestamp"]
                    latest = sp
            if not latest:
                return {"error": "no_valid_savepoint"}
            self.current = latest

        # aplicar estado no engine (espera-se que engine aceite dict de estado)
        try:
            state = self.current.get("engine_state", {})
            # tentativa segura de restaurar atributos básicos
            for k, v in state.items():
                try:
                    setattr(engine, k, v)
                except Exception:
                    # pula atributos que não possam ser aplicados diretamente
                    pass
            return {"restored": True, "tag": self.current.get("tag")}
        except Exception as e:
            return {"error": "restore_failed", "detail": str(e)}

if __name__ == "__main__":
    # demo rápido
    sp = A2F2_Savepoint()
    demo_state = {"estado": "demo", "history_len": 0}
    created = sp.criar(demo_state, tag="demo_save")
    print("Criado:", created)
    print("Listagem:", sp.listar())
    loaded = sp.carregar("demo_save")
    print("Carregado:", loaded)
