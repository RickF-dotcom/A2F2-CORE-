# A2F2 — Storage Handler
# Arquivo: a2f2-storage.py
# Versão: 0.1
#
# Camada de armazenamento local simples (baseada em arquivos JSON)
# Usada por: Savepoint, Config, Logs, Buffers, etc.

import os
import json

class A2F2_Storage:
    def __init__(self, base="a2f2_data"):
        self.base = base
        # cria diretório se não existir
        if not os.path.exists(self.base):
            try:
                os.makedirs(self.base)
            except Exception as e:
                print("Erro ao criar diretório base:", e)

    def _path(self, name):
        # todos arquivos terminam em .json
        return os.path.join(self.base, f"{name}.json")

    # -----------------------------------------------------------
    # SALVAR
    # -----------------------------------------------------------
    def salvar(self, name, data):
        try:
            caminho = self._path(name)
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            return {"error": "save_exception", "detail": str(e)}

    # -----------------------------------------------------------
    # CARREGAR
    # -----------------------------------------------------------
    def carregar(self, name):
        try:
            caminho = self._path(name)
            if not os.path.exists(caminho):
                return {"error": "file_not_found", "file": name}

            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            return {"error": "load_exception", "detail": str(e)}

    # -----------------------------------------------------------
    # LISTAR
    # -----------------------------------------------------------
    def listar(self):
        try:
            return [f for f in os.listdir(self.base) if f.endswith(".json")]
        except Exception as e:
            return {"error": "list_exception", "detail": str(e)}

    # -----------------------------------------------------------
    # APAGAR
    # -----------------------------------------------------------
    def deletar(self, name):
        try:
            caminho = self._path(name)
            if os.path.exists(caminho):
                os.remove(caminho)
                return True
            return {"error": "file_not_found", "file": name}
        except Exception as e:
            return {"error": "delete_exception", "detail": str(e)}

if __name__ == "__main__":
    sto = A2F2_Storage()
    print("Arquivos:", sto.listar())
