# a2f2-healthcheck.py
# Healthcheck simples do A2F2.
# - Se Flask estiver disponível, expõe /a2f2/health como endpoint HTTP.
# - Se não houver Flask, apenas imprime um JSON simples no stdout (útil para One-off shell).

import json
import time

def health_payload(uptime_seconds: int = 0):
    return {
        "status": "ok",
        "service": "A2F2",
        "uptime_seconds": int(uptime_seconds)
    }

def run_check():
    payload = health_payload(0)
    print(json.dumps(payload))

if __name__ == "__main__":
    try:
        # tenta expor endpoint HTTP se Flask estiver instalado
        from flask import Flask, jsonify
        import threading, sys

        app = Flask("a2f2_health")

        @app.route("/a2f2/health", methods=["GET"])
        def _health():
            return jsonify(health_payload( int(time.time() % 1000) ))

        # se executar sem argumentos, apenas imprime o check e sai
        if len(sys.argv) == 1:
            run_check()
        else:
            # se for chamado com "serve", inicia o server HTTP (porta 10000)
            if sys.argv[1] == "serve":
                app.run(host="0.0.0.0", port=10000)
            else:
                run_check()

    except Exception:
        # Flask não disponível — apenas execução CLI de verificação
        run_check()
