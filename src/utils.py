from enum import Enum

# Definindo o host e a porta em que o servidor irá se conectar aos clients
HOST = '127.0.0.1'
PORT = 7667

# Definindo uma enumeração chamada OperacaoBancaria
class OperacaoBancaria(Enum):
    SALDO = 0
    DEPOSITO = 1
    SAQUE = 2
    TRANSFERENCIA = 3
    DESCONECTAR = 99

# Definindo uma enumeração chamada OrigemRequisicao
class OrigemRequisicao(Enum):
    CAIXA_ELETRONICO = '[Caixa Eletrônico]'
    SERVIDOR_BANCO = '[Servidor Bancário]'

# Funções auxiliares
def printar_valor_relogio_logico(origem, tempo):
    """Função para imprimir o valor do relógio lógico."""
    mensagem = "{} - Valor atual do relógio lógico: {}."
    print(mensagem.format(origem, tempo))