menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Valor para depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Falha! Valor inválido.")

    elif opcao == "s":
        valor = float(input("Valor para saque: "))

        saldo_insuficiente = valor > saldo
        acima_limite = valor > limite
        saques_excedidos = numero_saques >= LIMITE_SAQUES

        if saldo_insuficiente:
            print("Falha! Saldo insuficiente.")
        elif acima_limite:
            print("Falha! Valor excede o limite.")
        elif saques_excedidos:
            print("Falha! Limite de saques atingido.")
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
        else:
            print("Falha! Valor inválido.")

    elif opcao == "e":
        print("\n========== EXTRATO ==========")
        print(extrato if extrato else "Sem movimentações.")
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("=============================")

    elif opcao == "q":
        break

    else:
        print("Opção inválida, tente novamente.")
