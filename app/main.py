from flask import Blueprint, current_app, request, jsonify
from sqlalchemy.orm.exc import NoResultFound
from marshmallow.exceptions import ValidationError

from .model import AIModel, db
from .serializer import AIModelSchema


bp_aimodels = Blueprint('aimodels', __name__)

@bp_aimodels.route('/modelo', methods=['GET'])
def fetch_all():
    result = AIModel.query.all()
    aims = AIModelSchema(many=True)
    return aims.jsonify(result), 200


@bp_aimodels.route('/modelo/<nome>', methods=['GET'])
def get_model(nome):
    try:
        result = AIModel.query.filter_by(nome=nome).one()
        aims = AIModelSchema()
        aimodel = aims.dump(result)
        return jsonify(aimodel), 200

    except NoResultFound:
        return jsonify({'error': 'No such model found within the database'}), 404


@bp_aimodels.route('/modelo', methods=['POST'])
def create_model():
    try:
        aims = AIModelSchema()
        aimodel = aims.load(request.json, session=db.session)
        current_app.db.session.add(aimodel)
        current_app.db.session.commit()
        return aims.jsonify(aimodel), 201

    except ValidationError:
        return jsonify({'error': 'Invalid input'}), 401
