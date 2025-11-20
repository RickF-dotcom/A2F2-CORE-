# test_import_motor.py
# Teste simples de importação do wrapper motor_a2f2

import importlib, sys, traceback

try:
    m = importlib.import_module("motor_a2f2")
    Motor = getattr(m, "Motor", None)
    MotorA2F2 = getattr(m, "MotorA2F2", None)
    print("IMPORT_OK")
    print("m.__file__:", getattr(m, "__file__", None))
    print("Motor:", Motor)
    print("MotorA2F2:", MotorA2F2)
except Exception:
    print("IMPORT_FAIL")
    traceback.print_exc()
    print("sys.path:", sys.path)
