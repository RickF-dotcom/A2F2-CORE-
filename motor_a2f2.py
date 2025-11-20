# motor_a2f2.py
# Wrapper oficial do motor A2F2 — implementa/exporta MotorA2F2 para o ecossistema

from a2f2_engine import A2F2Engine

class MotorA2F2(A2F2Engine):
    """Wrapper vazio/compatibilidade: o 'motor' do repositório espera MotorA2F2."""
    pass

# Alias comum usado em alguns módulos
Motor = MotorA2F2
