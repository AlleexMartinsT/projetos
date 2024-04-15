from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Acoes(db.Model):
    __tablename__ = 'acoes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sigla = db.Column(db.String(10), nullable=False)
    logo = db.Column(db.String(100))

    def __repr__(self):
        return f"Acoes(id={self.id}, nome={self.nome}, sigla={self.sigla}, logo={self.logo})"
