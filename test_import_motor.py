print("\n=== INÍCIO DO TESTE DO MOTOR A2F2 ===")

try:
    print("Importando núcleo do motor...")
    import a2f2_motor  # ajuste depois se o nome do motor for outro
    print("Módulo importado com sucesso.")
except Exception as e:
    print("ERRO ao importar o motor:")
    print(e)

print("=== FIM DO TESTE DO MOTOR A2F2 ===\n")
