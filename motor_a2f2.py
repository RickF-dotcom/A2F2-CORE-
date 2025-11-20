# motor_a2f2.py
# Wrapper oficial do motor A2F2 — importa a classe principal do engine

from a2f2_engine import A2F2Engine

class MotorA2F2(A2F2Engine):
    """Wrapper vazio para compatibilidade com importações antigas."""
    pass

# alias compatível
Motor = MotorA2F2
