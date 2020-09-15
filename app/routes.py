from flask import Blueprint, current_app, request, jsonify
from .model import AIModel, db
from .serializer import AIModelSchema

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from marshmallow.exceptions import ValidationError


# Register main blueprint
bp_aimodels = Blueprint('aimodels', __name__)


@bp_aimodels.route('/modelo', methods=['GET'])
def fetch_all():
    """Returns all models stored in the database"""
    # Perform a query to get all available data
    result = AIModel.query.all()
    # Create a serializer schema with relevant info only
    aims = AIModelSchema(many=True, only=('nome', 'descricao'))
    # De-serialize result and return json along with http transaction status code
    return aims.jsonify(result), 200


@bp_aimodels.route('/modelo/<nome>', methods=['GET'])
def get_model(nome):
    """Returns the model based on user query"""
    try:
        # Perform a query to return a row containing provided name
        result = AIModel().query.filter_by(nome=nome).one()
        # Create a serializer schema with relevant info only
        aims = AIModelSchema(only=('nome', 'descricao'))
        # De-serialize the query result
        aimodel = aims.dump(result)
        # Return json along with http transaction status code
        return jsonify(aimodel), 200

    except NoResultFound:
        # If given name is not found, return json with error message and http status code 
        return jsonify({'error': 'No such model found within the database'}), 404


@bp_aimodels.route('/modelo', methods=['POST'])
def create_model():
    """Creates a new model and saves it to database"""
    try:
        # Create a serializer schema
        aims = AIModelSchema(only=('nome', 'descricao'))
        # Serialize payload data to defined schema
        aimodel = aims.load(request.json, session=db.session)
        # Perform db transaction to add model
        current_app.db.session.add(aimodel)
        current_app.db.session.commit()
        # Return de-serialized json data along with http status code 
        return aims.jsonify(aimodel), 201

    except ValidationError:
        # If user provides payload with incorrect format, return error message with status code
        return jsonify({'error': 'Invalid input'}), 400

    except IntegrityError:
        # If user provides an already existing name, return error message with status code
        return jsonify({'error': 'Given name already found within the database'}), 409
