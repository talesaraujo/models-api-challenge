from flask_sqlalchemy import SQLAlchemy

# Create orm instance
db = SQLAlchemy()

def configure(app):
    """Connects ORM to main application"""
    db.init_app(app)
    app.db = db

class AIModel(db.Model):
    # Define model's SQL table and attributes
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)
    descricao = db.Column(db.String(255))
