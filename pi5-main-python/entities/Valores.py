from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Valores(db.Model):
    __tablename__ = 'valores'

    id = db.Column(db.Integer, primary_key=True)
    acao_id = db.Column(db.Integer, db.ForeignKey('acoes.id'), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    valor_fechamento = db.Column(db.Float, nullable=False)
    valor_abertura = db.Column(db.Float, nullable=False)
    valor_alta = db.Column(db.Float, nullable=False)
    valor_baixa = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Valores(id={self.id}, acao_id={self.acao_id}, data={self.data}, valor_fechamento={self.valor_fechamento}, valor_abertura={self.valor_abertura}, valor_alta={self.valor_alta}, valor_baixa={self.valor_baixa})"
