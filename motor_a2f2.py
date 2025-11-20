# motor_a2f2.py
# Wrapper oficial do motor A2F2
# Este arquivo conecta o motor REAL ao nome padrão do ecossistema.

from a2f2_engine import A2F2Engine

# Classe com o nome que o ecossistema A2F2 espera
class MotorA2F2(A2F2Engine):
    pass

# Alias adicional (alguns módulos procuram "Motor")
Motor = MotorA2F2
