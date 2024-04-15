from flask import Blueprint, jsonify

acoes_blueprint = Blueprint('acoes', __name__, url_prefix='/api/acoes')

class AcoesController:
    def __init__(self, acoes_service):
        self.acoes_service = acoes_service

    # rota de teste
    @acoes_blueprint.route('/teste')
    def teste():
        return "Ei"

    # rota para atualizar os dados das ações
    @acoes_blueprint.route('/atualizar-dados', methods=['POST'])
    def atualizar_dados():
        # lógica para chamar o serviço para atualizar os dados das ações
        return jsonify(message="Dados atualizados com sucesso!")

