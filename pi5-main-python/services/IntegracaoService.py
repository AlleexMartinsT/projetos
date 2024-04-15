import requests
from typing import Dict

class IntegracaoService:
    def __init__(self, token: str, url_padrao: str):
        self.token = token
        self.url_padrao = url_padrao

    def get_dados(self, caminho: str, nome_acao: str) -> Dict:
        # montando a URL
        url = f"{self.url_padrao}/{caminho}/{nome_acao}?range=3mo&interval=1d&fundamental=true&token={self.token}"
        
        # solicitação HTTP
        response = requests.get(url)
        
        # Verificando se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Analisando a resposta JSON
            return response.json()
        else:
            # lidando com erros de solicitação
            response.raise_for_status()

# exemplo (>testar se deu certo<)
if __name__ == "__main__":
    # criando uma instância do serviço de integração com os dados de configuração
    integracao_service = IntegracaoService(token="seu_token_aqui", url_padrao="sua_url_padrao_aqui")

    # obtendo dados de exemplo
    caminho = "quote"
    nome_acao = "TSLA34"
    dados = integracao_service.get_dados(caminho, nome_acao)

    # exibindo os dados obtidos
    print(dados)
