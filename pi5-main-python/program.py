from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurando o banco de dados
app.config['banco de dados SQLALCHEMY'] = 'cnn aq'
db = SQLAlchemy(app)

# modelos
class Acao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)

class Integracao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)

# serviços
class AcoesService:
    def listar_acoes(self):
        return Acao.query.all()

class IntegracaoService:
    def listar_integracoes(self):
        return Integracao.query.all()

# rotas
@app.route('/acoes')
def listar_acoes():
    service = AcoesService()
    acoes = service.listar_acoes()
    return {'acoes': [{'nome': acao.nome, 'descricao': acao.descricao} for acao in acoes]}

@app.route('/integracoes')
def listar_integracoes():
    service = IntegracaoService()
    integracoes = service.listar_integracoes()
    return {'integracoes': [{'nome': integracao.nome, 'descricao': integracao.descricao} for integracao in integracoes]}

if __name__ == '__main__':
    app.run(debug=True)
