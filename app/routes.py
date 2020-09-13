from flask import Blueprint, current_app, request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from marshmallow.exceptions import ValidationError

from .model import AIModel, db
from .serializer import AIModelSchema


bp_aimodels = Blueprint('aimodels', __name__)


@bp_aimodels.route('/modelo', methods=['GET'])
def fetch_all():
    result = AIModel.query.all()
    aims = AIModelSchema(many=True, only=('nome', 'descricao'))
    return aims.jsonify(result), 200


@bp_aimodels.route('/modelo/<nome>', methods=['GET'])
def get_model(nome):
    try:
        result = AIModel().query.filter_by(nome=nome).one()
        aims = AIModelSchema(only=('nome', 'descricao'))
        aimodel = aims.dump(result)
        return jsonify(aimodel), 200

    except NoResultFound:
        return jsonify({'error': 'No such model found within the database'}), 404


@bp_aimodels.route('/modelo', methods=['POST'])
def create_model():
    try:
        aims = AIModelSchema(only=('nome', 'descricao'))
        aimodel = aims.load(request.json, session=db.session)
        current_app.db.session.add(aimodel)
        current_app.db.session.commit()
        return aims.jsonify(aimodel), 201

    except ValidationError:
        return jsonify({'error': 'Invalid input'}), 400

    except IntegrityError:
        return jsonify({'error': 'Given name already found within the database'}), 409
