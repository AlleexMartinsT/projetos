from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PI5Context(db.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sigla = db.Column(db.String(10), nullable=False)
    logo = db.Column(db.String(100))

    acoes = db.relationship('Acoes', backref='pi5_context', lazy=True)
    valores = db.relationship('Valores', backref='pi5_context', lazy=True)

    def __repr__(self):
        return f"PI5Context(id={self.id}, nome={self.nome}, sigla={self.sigla}, logo={self.logo})"
