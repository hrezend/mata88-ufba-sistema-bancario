from enum import Enum

# Definindo constantes de utilidades e configurações
HOST = '127.0.0.1'
PORT = 7667
MAX_CLIENTS_CONNECTED = 5
CONTAS_CORRENTES_DEFAULT = {'05471175581': {'nome': 'Herson Rezende', 'saldo': 0.0}, '00000000000': {'nome': 'Kennedy Anderson', 'saldo': 0.0}}

# Definindo uma enumeração chamada OperacaoBancaria
class OperacaoBancaria(Enum):
    SALDO = '0'
    DEPOSITO = '1'
    SAQUE = '2'
    TRANSFERENCIA = '3'
    DESCONECTAR = '99'

# Definindo uma enumeração chamada OrigemRequisicao
class OrigemRequisicao(Enum):
    CAIXA_ELETRONICO = '[Caixa Eletrônico]'
    SERVIDOR_BANCO = '[Servidor Bancário]'

class StatusRequisicao(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

# Funções auxiliares
def printar_valor_relogio_logico(origem, tempo):
    """Função para imprimir o valor do relógio lógico."""
    mensagem = "{} - Valor atual do relógio lógico: {}."
    print(mensagem.format(origem, tempo))