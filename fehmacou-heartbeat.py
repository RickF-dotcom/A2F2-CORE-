# FEHMACOU — Heartbeat Monitor
# Versão: 0.1
# Arquivo: fehmacou-heartbeat.py

import time

class FEHMACOUHeartbeat:

    def __init__(self):
        self.last_pulse = None
        self.pulse_history = []

    def pulse(self):
        timestamp = time.time()
        self.last_pulse = timestamp
        self.pulse_history.append(timestamp)
        return {
            "status": "ALIVE",
            "timestamp": timestamp
        }

    def get_last_pulse(self):
        return self.last_pulse

    def get_pulse_history(self):
        return self.pulse_history

    def status(self):
        if not self.last_pulse:
            return "NO_PULSE_RECORDED"
        
        diff = time.time() - self.last_pulse
        
        if diff < 5:
            return "STABLE"
        elif diff < 20:
            return "LATE"
        else:
            return "INACTIVE"
