from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db

class AIModel(db.Model):
    nome = db.Column(db.String(255), primary_key=True)
    descricao = db.Column(db.String(255))
