from enum import Enum

# Definindo uma enumeração chamada OperacaoBancaria
class OperacaoBancaria(Enum):
    SALDO = 0
    DEPOSITO = 1
    SAQUE = 2
    TRANSFERENCIA = 3
    DESCONECTAR = 99

# Definindo o host e a porta em que o servidor irá se conectar aos clients
HOST = '127.0.0.1'
PORT = 7667