## Trabalho de MATA88 - Sistemas Distribuídos (2023.2)

### Grupo: Hérson Rezende e Kennedy Anderson
### Docente: Raimundo José de Araújo Macêdo
</br>

A **especificação** do trabalho pode ser encontrada [aqui](assets/especificacao.pdf).

A descrição da **solução** elaborada pelo grupo pode ser encontrada [aqui](assets/solucao.pdf).

A **apresentação** do grupo, em slides, pode ser encontrada [aqui](assets/apresentacao.pdf).

O **repositório** oficial no github pode ser encontrado [aqui](https://github.com/hrezend/mata88-ufba-sistema-bancario).

---

### Como executar este código?
- Antes de tudo, é necessário que você possua o ambiente de desenvolvimento configurado para trabalhar com [python3](https://www.python.org/downloads/) em sua máquina.
  1. Observe que a implementação está na pasta `src` da raiz do projeto. Para executar o projeto, é preciso inicializar um terminal e entrar nesta pasta `($cd /src)`.
  2. Inicialize um terminal e execute o comando `py server.py` para executar o servidor da aplicação que, neste caso, será análogo a um servidor bancário. 
  3. Inicialize outro terminal e execute o comando `py client.py` para rodar um client da aplicação que, neste caso, será análogo a um caixa eletrônico. Em seguida, responda aos inputs solicitados pelo programa.

- Não é necessário executar o arquivo `utils.py`, pois ele se trata apenas funções auxiliares e constantes que são importadas pelos arquivos supracitados.

- Caso ainda não exista, na primeira execução do programa um arquivo chamado `contas_correntes.json` será criado. Este, servirá como "base de dados" para manter as contas e o saldo de cada uma delas.
  - É aconselhável **não fazer alterações diretas neste arquivo**, pois pode impactar no funcionamento da aplicação.