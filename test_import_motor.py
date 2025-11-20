# test_import_motor.py
# Teste simples para verificar se motor_a2f2 importa corretamente

import importlib, sys

try:
    m = importlib.import_module("motor_a2f2")
    Motor = getattr(m, "Motor", None)
    MotorA2F2 = getattr(m, "MotorA2F2", None)

    print("IMPORT_OK")
    print("Módulo motor_a2f2:", getattr(m, "__file__", "<nenhum>"))
    print("Motor:", Motor)
    print("MotorA2F2:", MotorA2F2)

except Exception as e:
    print("IMPORT_FAIL")
    import traceback
    traceback.print_exc()
    print("sys.path:", sys.path)
