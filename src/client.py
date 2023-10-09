import socket
import json
import sys
from utils import OperacaoBancaria, OrigemRequisicao, HOST, PORT, printar_valor_relogio_logico

# Configurações iniciais do cliente
client_socket = socket.socket()
time = 0

def printar_valor_relogio_logico(time):
    """Função para imprimir o valor do relógio lógico."""
    mensagem = "[Caixa Eletrônico] - Valor atual do relógio lógico: {}."
    print(mensagem.format(time))

def ajustar_valor_relogio_logico(server_time):
    """Função para ajustar o valor do relógio lógico com base no timer do server."""
    global time
    time = max(time, int(server_time)) + 1
    printar_valor_relogio_logico(OrigemRequisicao.CAIXA_ELETRONICO.value, time)

def incrementar_valor_relogio_logico():
    """Função para incrementar o valor do relógio lógico."""
    global time
    time += 1
    printar_valor_relogio_logico(OrigemRequisicao.CAIXA_ELETRONICO.value, time)

def estabelecer_conexao():
    """Estabelece a conexão com o servidor."""
    try:
        client_socket.connect((HOST, PORT))
    except socket.error as err:
        print("[Caixa Eletrônico] - Não foi possível estabelecer a conexão com o banco... Tente novamente mais tarde!")
        print(str(err))
        sys.exit(1)

def enviar_mensagem(data):
    """Envia uma mensagem ao servidor."""
    incrementar_valor_relogio_logico()
    body = json.dumps(data)
    client_socket.send(body.encode('utf-8'))

def receber_resposta():
    """Recebe a resposta do servidor."""
    response = client_socket.recv(1024).decode('utf-8')
    body = json.loads(response)
    ajustar_valor_relogio_logico(body['time'])
    return body

def main():
    # Realiza conexão inicial com o servidor
    estabelecer_conexao()

    # Receber resposta inicial do servidor
    resposta_inicial = receber_resposta()
    print(resposta_inicial['message'])

    # Enviar RG/CPF ao servidor
    identificador_pessoa = input('[Caixa Eletrônico] - Digite seu CPF ou RG:')
    enviar_mensagem({'identificador_origem': identificador_pessoa, 'time': time})
    resposta_identificador = receber_resposta()
    print(resposta_identificador['message'])

    while True:
        print("[Caixa Eletrônico] - Escolha uma das operações abaixo:")
        for operacao in OperacaoBancaria:
            print(f"{operacao.value}. {operacao.name.capitalize()}")
        op = input()

        if op == OperacaoBancaria.SALDO.value:
            print('[Caixa Eletrônico] - Consultando saldo...')
            enviar_mensagem({'time': time, 'operation': op})
            resposta_saldo = receber_resposta()
            print(resposta_saldo['message'])
        elif op == OperacaoBancaria.SAQUE.value:
            saque = input('[Caixa Eletrônico] - Digite o valor que deseja sacar:')
            enviar_mensagem({'time': time, 'operation': op, 'value': saque})
            resposta_saque = receber_resposta()
            print(resposta_saque['message'])
        elif op == OperacaoBancaria.DEPOSITO.value:
            deposito = input('[Caixa Eletrônico] - Digite o valor que deseja depositar:')
            enviar_mensagem({'time': time, 'operation': op, 'value': deposito})
            resposta_deposito = receber_resposta()
            print(resposta_deposito['message'])
        elif op == OperacaoBancaria.TRANSFERENCIA.value:
            identificador_transferencia = input('[Caixa Eletrônico] - Digite o identificador da conta para a qual quer transferir:')
            value_transferencia = input('[Caixa Eletrônico] - Digite o valor que deseja transferir:')
            enviar_mensagem({'identificador_destino': identificador_transferencia, 'time': time, 'operation': op, 'value': value_transferencia})
            resposta_transferencia = receber_resposta()
            print(resposta_transferencia['message'])
        elif op == OperacaoBancaria.DESCONECTAR.value:
            print("[Caixa Eletrônico] - Obrigado por utilizar os nossos serviços!")
            enviar_mensagem({'time': time, 'operation': op})
            client_socket.close()
            break
        else:
            print("[Caixa Eletrônico] - Comando inválido, tente novamente!")

if __name__ == "__main__":
    main()
