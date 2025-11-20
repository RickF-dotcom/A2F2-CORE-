# motor_a2f2.py
# Wrapper oficial do motor A2F2
# Este arquivo conecta o motor REAL (A2F2Engine) ao nome padrão usado pelo ecossistema.

from a2f2_engine import A2F2Engine

class MotorA2F2(A2F2Engine):
    pass

# Alias extra para compatibilidade
Motor = MotorA2F2
