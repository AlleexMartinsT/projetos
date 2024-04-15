from abc import ABC, abstractmethod

class IAcoesService(ABC):
    @abstractmethod
    def atualiza_dados(self):
        pass
