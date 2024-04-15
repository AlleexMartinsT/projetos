from abc import ABC, abstractmethod
from typing import Dict, Any

class IIntegracaoService(ABC):
    @abstractmethod
    def get_dados(self, caminho: str, nome_acao: str) -> Dict[str, Any]:
        pass
