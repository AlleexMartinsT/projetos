from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)
app.config['sqlachemy banco'] = 'cnn aq'
db = SQLAlchemy(app)

# modelos
class Acao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(100))
    sigla = db.Column(db.String(10), nullable=False)
    valores = db.relationship('Valor', backref='acao', lazy=True)

class Valor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acao_id = db.Column(db.Integer, db.ForeignKey('acao.id'), nullable=False)
    valor_fechamento = db.Column(db.Float, nullable=False)
    valor_abertura = db.Column(db.Float, nullable=False)
    valor_alta = db.Column(db.Float, nullable=False)
    valor_baixa = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False)

# serviços
class AcoesService:
    def atualiza_dados(self):
        # simulando a obtenção de dados
        retorno_dados = requests.get("sua_url_de_api_aqui").json()

        # processamento dos dados obtidos
        for resultado in retorno_dados['Results']:
            acao = Acao.query.filter_by(nome=resultado['LongName']).first()

            if not acao:
                acao = Acao(
                    nome=resultado['LongName'],
                    logo=resultado['LogoUrl'],
                    sigla=resultado['Symbol']
                )
                db.session.add(acao)
                db.session.commit()

            valores_banco = Valor.query.filter_by(acao_id=acao.id).all()

            for valor_api in resultado['HistoricalDataPrice']:
                data = datetime.fromtimestamp(valor_api['Data'])

                if not valores_banco or data not in [v.data for v in valores_banco]:
                    valor = Valor(
                        acao_id=acao.id,
                        valor_fechamento=valor_api['Close'],
                        valor_abertura=valor_api['Open'],
                        valor_alta=valor_api['High'],
                        valor_baixa=valor_api['Low'],
                        data=data
                    )
                    db.session.add(valor)
                    db.session.commit()

# rotas
@app.route('/atualizar_acoes')
def atualizar_acoes():
    service = AcoesService()
    service.atualiza_dados()
    return 'Dados atualizados com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)
