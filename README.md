# AIModels REST API Challenge
[Também disponível em Português](docs/LEIAME.md)

## Description
This is a Python Flask project that intends to provide a management service of data science/artificial inteligence models through a REST API. It has been structured with a three-tier architecture by using three main components: the main application, build with [Flask](https://flask.palletsprojects.com/en/1.1.x/), the [SQLAlchemy](https://www.sqlalchemy.org) [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping) toolkit for database management and the [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) library to [object serialization](https://en.wikipedia.org/wiki/Serialization).  

## Available endpoints

### `GET /modelo`
Returns all models and their respective descriptions.

### `GET /modelo/<nome-do-modelo>`
Returns only the model and the description from the name passed in as a URL parameter.

### `POST /modelo`
Creates a new model based on request payload.

### `DELETE /modelo/<nome-do-modelo>`
Removes a model from the database. The name of the model is used as a query parameter.

## Demo
Here's a sample of a json file managed by the API ("nome" stands for name and "descricao" stands for description):
```json
{
    "nome": "cat-vs-dogs-classifier",
    "descricao": "Convolutional neural network that classifies dogs and cat images, having 2 convolutional, 2 pooling and 3 fully-connected layers"
}
```

## How to run this project
First off, you must have [Python](https://www.python.org/) 3 installed. [Here](https://www.python.org/downloads) you can find links to the latest builds for your operating system.

In order to manage dependencies and virtual environments, I recommend using [`pipenv`](https://pypi.org/project/pipenv) if you intend to modify/provide improvements to the code, although `pip` will also work if you choose to do so. 
Switch to the project directory and install all the requirements afterwards:
```sh
pip install -r requirements.txt 
```
Then export the application's environment variables:
```sh
export FLASK_APP=app
export FLASK_ENV=development
export FLASK_DEBUG=True
```
Execute the database migrations:
```sh
flask db init
flask db migrate
flask db upgrade
```
The application is set to receive requests on port 5000. You can run it by issuing the command
```sh
flask run
```

## How to run tests
Having Python installed, simply run
```sh
python -m unittest tests/tests_api.py
```