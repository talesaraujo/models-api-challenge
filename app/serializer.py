from marshmallow import fields, ValidationError
from flask_marshmallow import Marshmallow
from .model import AIModel


ma = Marshmallow()

def configure(app):
    ma.init_app(app)


class AIModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AIModel
        load_instance = True

    nome = fields.Str(required=True)
    descricao = fields.Str(required=True)
