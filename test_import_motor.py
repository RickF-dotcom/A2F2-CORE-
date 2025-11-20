# test_import_motor.py
# Teste simples para verificar se motor_a2f2 importa corretamente

try:
    from motor_a2f2 import MotorA2F2
    print("IMPORT_OK: MotorA2F2 encontrado")
    print("MotorA2F2:", MotorA2F2)
except Exception as e:
    print("IMPORT_FAIL")
    print(type(e).__name__, str(e))
