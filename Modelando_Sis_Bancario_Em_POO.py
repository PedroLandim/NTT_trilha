from abc import ABC, abstractmethod
from datetime import datetime


# Classe Cliente conforme UML
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        if conta in self.contas:
            transacao.registrar(conta)
        else:
            print("Conta não pertence ao cliente")


# Cliente Pessoa Física que herda de Cliente
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


# Classe Conta base
class Conta:
    def __init__(self, cliente, numero, agencia='0001'):
        self._saldo = 0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso.")
            return True
        print("Valor de depósito inválido.")
        return False

    def sacar(self, valor):
        if 0 < valor <= self._saldo:
            self._saldo -= valor
            print("Saque realizado com sucesso.")
            return True
        print("Saldo insuficiente ou valor inválido.")
        return False

    @property
    def saldo(self):
        return self._saldo

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)


# Conta Corrente que herda de Conta
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def sacar(self, valor):
        if self.saques_realizados >= self.limite_saques:
            print("Limite de saques atingido.")
            return False
        if valor > self.limite:
            print("Valor do saque excede o limite permitido.")
            return False
        if super().sacar(valor):
            self.saques_realizados += 1
            return True
        return False


# Classe para Histórico de Transações
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })


# Interface de Transações conforme UML
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


# Classe de Saque
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


# Classe de Depósito
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


# Funções de apoio para as operações bancárias
def filtrar_cliente(clientes, cpf):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None


def exibir_extrato(conta):
    print("\nExtrato da Conta:")
    for transacao in conta.historico.transacoes:
        print(f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")
    print(f"Saldo atual: R$ {conta.saldo:.2f}")


# Função para mostrar o menu de operações
def mostrar_menu():
    print("\n=== Menu de Operações Bancárias ===")
    print("1. Criar nova conta")
    print("2. Realizar depósito")
    print("3. Realizar saque")
    print("4. Exibir extrato")
    print("5. Sair")
    return int(input("Escolha uma opção: "))


# Exemplo de operação usando o código reformulado
def main():
    clientes = []
    contas = []

    while True:
        opcao = mostrar_menu()

        if opcao == 1:
            # Criar novo cliente e conta
            nome = input("Digite o nome do cliente: ")
            cpf = input("Digite o CPF: ")
            data_nascimento = input("Digite a data de nascimento (DD/MM/AAAA): ")
            endereco = input("Digite o endereço: ")
            cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
            clientes.append(cliente)

            numero_conta = int(input("Digite o número da nova conta: "))
            conta = ContaCorrente(cliente, numero_conta)
            cliente.adicionar_conta(conta)
            contas.append(conta)
            print("Conta criada com sucesso!")

        elif opcao == 2:
            # Realizar depósito
            cpf = input("Digite o CPF do cliente: ")
            cliente = filtrar_cliente(clientes, cpf)
            if cliente:
                numero_conta = int(input("Digite o número da conta para depósito: "))
                conta = next((c for c in cliente.contas if c.numero == numero_conta), None)
                if conta:
                    valor = float(input("Digite o valor do depósito: "))
                    deposito = Deposito(valor)
                    cliente.realizar_transacao(conta, deposito)
                else:
                    print("Conta não encontrada.")
            else:
                print("Cliente não encontrado.")

        elif opcao == 3:
            # Realizar saque
            cpf = input("Digite o CPF do cliente: ")
            cliente = filtrar_cliente(clientes, cpf)
            if cliente:
                numero_conta = int(input("Digite o número da conta para saque: "))
                conta = next((c for c in cliente.contas if c.numero == numero_conta), None)
                if conta:
                    valor = float(input("Digite o valor do saque: "))
                    saque = Saque(valor)
                    cliente.realizar_transacao(conta, saque)
                else:
                    print("Conta não encontrada.")
            else:
                print("Cliente não encontrado.")

        elif opcao == 4:
            # Exibir extrato
            cpf = input("Digite o CPF do cliente: ")
            cliente = filtrar_cliente(clientes, cpf)
            if cliente:
                numero_conta = int(input("Digite o número da conta para exibir extrato: "))
                conta = next((c for c in cliente.contas if c.numero == numero_conta), None)
                if conta:
                    exibir_extrato(conta)
                else:
                    print("Conta não encontrada.")
            else:
                print("Cliente não encontrado.")

        elif opcao == 5:
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
