# motor_a2f2.py
# Wrapper compatível para expor MotorA2F2 quando o código real está em a2f2-engine.py
# (resolve problema de nomes com hífen em import padrão)

import importlib.util
import pathlib
import sys

# localiza o arquivo a2f2-engine.py no mesmo diretório deste wrapper
_here = pathlib.Path(__file__).parent
_engine_path = _here / "a2f2-engine.py"

if not _engine_path.exists():
    raise ImportError(f"Arquivo esperado não encontrado: {_engine_path!s}")

spec = importlib.util.spec_from_file_location("a2f2_engine_impl", str(_engine_path))
_engine_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_engine_mod)

# tenta pegar a classe / factory com nomes prováveis
if hasattr(_engine_mod, "MotorA2F2"):
    MotorA2F2 = getattr(_engine_mod, "MotorA2F2")
elif hasattr(_engine_mod, "Motor"):
    MotorA2F2 = getattr(_engine_mod, "Motor")
else:
    # se o módulo não tiver uma das referências, expõe tudo para facilitar debug
    # e lança erro claro
    globals().update({n: getattr(_engine_mod, n) for n in dir(_engine_mod) if not n.startswith("_")})
    raise ImportError("Não foi encontrado 'MotorA2F2' nem 'Motor' em a2f2-engine.py. "
                      "Verifique o nome da classe no arquivo a2f2-engine.py.")
