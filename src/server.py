import os
import json
import socket
import threading
from _thread import start_new_thread
from json import JSONDecodeError
from utils import OperacaoBancaria, OrigemRequisicao, StatusRequisicao, HOST, PORT, CONTAS_CORRENTES_DEFAULT, MAX_CLIENTS_CONNECTED, printar_valor_relogio_logico

# Configurações Iniciais
time = 0
contas_correntes = {}
mutex_time = threading.Lock()
mutex_accounts = threading.Lock()
server_socket = socket.socket()
thread_count = 0
threads = []

def incrementar_relogio():
	global time
	mutex_time.acquire()
	time += 1
	printar_valor_relogio_logico(OrigemRequisicao.SERVIDOR_BANCO.value, time)
	mutex_time.release()

def incrementar_relogio_timestamp(timestamp, atual):
	global time
	mutex_time.acquire()
	time = max(timestamp,atual) + 1
	printar_valor_relogio_logico(OrigemRequisicao.SERVIDOR_BANCO.value, time)
	mutex_time.release()

def salvar_contas(contas_correntes):
	with open("contas_correntes.json", "w") as output_file:
		json.dump(contas_correntes, output_file)
	   
def carregar_contas():
	try:
		global contas_correntes
		with open("contas_correntes.json", "r") as input_file:
			contas_correntes = json.load(input_file)
	except (FileNotFoundError):
		print("{} - Não foi possível recuperar as contas correntes do arquivo.".format(OrigemRequisicao.SERVIDOR_BANCO.value))
		print("{} - Utilizaremos as contas default que estão disponíveis no arquivo 'utils.py'.".format(OrigemRequisicao.SERVIDOR_BANCO.value))
		contas_correntes = CONTAS_CORRENTES_DEFAULT
		salvar_contas(contas_correntes)
	return contas_correntes

def enviar_mensagem(connection, data):
    """Envia uma mensagem ao client conectado."""
    body = json.dumps(data)
    connection.send(body.encode('utf-8'))

def receber_resposta(connection):
	"""Recebe a resposta do client conectado."""
	try:
		response = connection.recv(1024).decode('utf-8')
		body = json.loads(response)
		return body
	except (JSONDecodeError):
		print("{} - Erro ao decodificar a mensagem recebida do client.".format(OrigemRequisicao.SERVIDOR_BANCO.value))
		return {'status': 500}

def threaded_client(connection):
	# Confirma a conexão realizada com o client.
	global time
	global contas_correntes
	incrementar_relogio()
	enviar_mensagem(connection, {'message': 'Conexão estabelecida com sucesso!', 'time': time, 'status': StatusRequisicao.OK.value})
	
	# Recebe do client o identificador da conta corrente.
	response = receber_resposta(connection)
	if response['status'] == 500:
		connection.close()
		return

	id_conta = response['identificador_origem']
	incrementar_relogio_timestamp(int(response['time']), time)
	incrementar_relogio()

	# Verifica se a chave da conta corrente recebida do client existe no dicionário.
	if id_conta in contas_correntes:
		text_message = OrigemRequisicao.SERVIDOR_BANCO.value + ' - Conta corrente encontrada.'
		enviar_mensagem(connection, {'message': text_message, 'time': time, 'status': StatusRequisicao.OK.value})
	else:
		text_message = OrigemRequisicao.SERVIDOR_BANCO.value + ' - Esta conta corrente não foi encontrada.'
		enviar_mensagem(connection, {'message': text_message, 'time': time, 'status': StatusRequisicao.NOT_FOUND.value})
		return

	while True:
		response = receber_resposta(connection)
		if response['status'] == 500:
			break

		if response['operation'] == OperacaoBancaria.SALDO.value:
			incrementar_relogio_timestamp(int(response['time']), time)
			carregar_contas()
			incrementar_relogio()
			incrementar_relogio()
			text_message = OrigemRequisicao.SERVIDOR_BANCO.value + ' - Saldo disponível: R$' + str(contas_correntes[id_conta]['saldo'])
			enviar_mensagem(connection, {'message': text_message, 'time': time, 'status': StatusRequisicao.OK.value})
		elif response['operation'] == OperacaoBancaria.DEPOSITO.value:
			incrementar_relogio_timestamp(int(response['time']), time)
			mutex_accounts.acquire()
			carregar_contas()
			contas_correntes[id_conta]['saldo'] += float(response['value'])
			salvar_contas(contas_correntes)
			mutex_accounts.release()
			incrementar_relogio()
			incrementar_relogio()
			text_message = OrigemRequisicao.SERVIDOR_BANCO.value + ' - Depósito realizado!'
			enviar_mensagem(connection, {'message': text_message, 'time': time, 'status': StatusRequisicao.CREATED.value})
		elif response['operation'] == OperacaoBancaria.SAQUE.value:
			incrementar_relogio_timestamp(int(response['time']),time)
			mutex_accounts.acquire()
			carregar_contas()
			contas_correntes[id_conta]['saldo'] -= float(response['value'])
			salvar_contas(contas_correntes)
			mutex_accounts.release()
			incrementar_relogio()
			incrementar_relogio()
			text_message = OrigemRequisicao.SERVIDOR_BANCO.value + ' - Saque realizado!'
			enviar_mensagem(connection, {'message': text_message, 'time': time, 'status': StatusRequisicao.CREATED.value})
		elif response['operation'] == OperacaoBancaria.TRANSFERENCIA.value:
			incrementar_relogio_timestamp(int(response['time']),time)
			mutex_accounts.acquire()
			carregar_contas()
			contas_correntes[id_conta]['saldo'] -= float(response['value'])
			contas_correntes[response['identificador_destino']]['saldo']+=float(response['value'])
			salvar_contas(contas_correntes)
			mutex_accounts.release()
			incrementar_relogio()
			incrementar_relogio()
			text_message = OrigemRequisicao.SERVIDOR_BANCO.value + ' - Transferência realizada!'
			enviar_mensagem(connection, {'message': text_message, 'time': time, 'status': StatusRequisicao.CREATED.value})
		elif response['operation'] == OperacaoBancaria.DESCONECTAR.value:
			incrementar_relogio_timestamp(int(response['time']),time)
			incrementar_relogio()
			text_message = OrigemRequisicao.SERVIDOR_BANCO.value + ' - Encerrando conexão...'
			enviar_mensagem(connection, {'message': text_message, 'time': time, 'status': StatusRequisicao.OK.value})
			break
	connection.close()

def inicializar_servidor():
	try:
		carregar_contas()
		server_socket.bind((HOST, PORT))
		print("{} - Aguardando conexão de clients... (MAX = {})".format(OrigemRequisicao.SERVIDOR_BANCO.value, MAX_CLIENTS_CONNECTED))
		server_socket.listen(MAX_CLIENTS_CONNECTED)
		global time
		time += 1
		printar_valor_relogio_logico(OrigemRequisicao.SERVIDOR_BANCO.value, time)
	except socket.error as err:
		print("{} - Não foi possível inicializar o servidor!", OrigemRequisicao.SERVIDOR_BANCO.value)
		print(str(err))

def main():
	inicializar_servidor()

	while True:
		try:
			client, address = server_socket.accept()
			print("{} - Conectado ao client {}:{}".format(OrigemRequisicao.SERVIDOR_BANCO.value, address[0], str(address[1])))
			threads.append(start_new_thread(threaded_client, (client, )))
			global thread_count
			thread_count += 1
			print("{} - Thread número: {}".format(OrigemRequisicao.SERVIDOR_BANCO.value, str(thread_count)))
		except (SystemExit, KeyboardInterrupt):
			break

	server_socket.close()

if __name__ == "__main__":
    main()
