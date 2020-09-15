from marshmallow import fields, validates, ValidationError
from flask_marshmallow import Marshmallow
from .model import AIModel

# Create serializer instance
ma = Marshmallow()

def configure(app):
    """Connects serializer to application"""
    ma.init_app(app)


class AIModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Assign orm model to serialization
        model = AIModel
        # Deserialize data to defined model instance
        load_instance = True

    # Define required schema variables
    nome = fields.Str(required=True)
    descricao = fields.Str(required=True)

    @validates('id')
    def validate_id(self, value):
        """Prevents user from sending id data"""
        raise ValidationError("Id must not be sent in")
