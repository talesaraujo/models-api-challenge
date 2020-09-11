from flask import Blueprint
from .model import AIModel
from .serializer import AIModelSchema


bp_aimodels = Blueprint('aimodels', __name__)

@bp_aimodels.route('/modelo', methods=['GET'])
def fetch_all():
    ais = AIModelSchema(many=True)
    result = AIModel.query.all()

    return ais.jsonify(result), 200


@bp_aimodels.route('/modelo/<nome>', methods=['GET'])
def get_model(nome):
    ...

@bp_aimodels.route('/modelo', methods=['POST'])
def create_model():
    ...
