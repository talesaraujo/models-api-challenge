# Desafio: REST API de modelos de IA

[Switch back to English version](../README.md)

## Descrição
Este é um projeto Python feito em Flask que procura fornecer um serviço de gerenciamento de modelos de data science/inteligência artificial por meio de uma API REST. Três componentes principais designam o serviço: a aplicação principal, feita em [Flask](https://flask-ptbr.readthedocs.io/en/latest), o toolkit [mapeador objeto-relacional](https://www.devmedia.com.br/orm-object-relational-mapper/19056) [SQLAlchemy](https://www.sqlalchemy.org) para o gerenciamento do banco de dados e a biblioteca [Marshmallow](https://marshmallow.readthedocs.io/en/stable) para a serialização de objetos. 

## Endpoints disponíveis

### `GET /modelo`
Retorna todos os modelos com suas respectivas descrições.

### `GET /modelo/<nome-do-modelo>`
Retorna somente o modelo e a descrição baseados no nome passado como parâmetro de URL

### `POST /modelo`
Cria um novo modelo baseado no payload da requisição

## Exemplo
Eis um exemplo de um arquivo json gerenciado pela API:
```json
{
    "nome": "cat-vs-dogs-classifier",
    "descricao": "Rede neural convolucional que classifica imagens de cães e gatos, com 2 camadas convolucionais, 2 de pooling e 3 tradicionais"
}
```

## Como executar este projeto
Primeiro de tudo, você precisará ter o [Python](https://www.python.org/) 3 instalado. [Aqui](https://www.python.org/downloads) você pode encontrar links dos os últimos lançamentos para o seu sistema operacional.

Visando um melhor gerenciamento de dependências e ambientes virtuais, eu recomendo usar o  [`pipenv`](https://pypi.org/project/pipenv) se você pretende modificar e/ou prover melhorias de código, mas o `pip` irá funcionar também se você preferir. 

Mude para o diretório do projeto e instale as dependências após isso:
```sh
pip install -r requirements.txt 
```
Feito isto, exporte as variáveis de ambiente da aplicação:
```sh
export FLASK_APP=app
export FLASK_ENV=development
export FLASK_DEBUG=True
```
Execute as migrações do banco de dados:
```sh
flask db init
flask db migrate
flask db upgrade
```
A aplicação está definida para receber requisições na porta 5000. Você poderá executá-la com o comando:
```sh
flask run
```

## Como executar os testes
Com o Python instalado, execute
```sh
python -m unittest tests/tests_api.py
```