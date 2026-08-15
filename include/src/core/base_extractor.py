# É uma classe abstrata.
# O que faz: Define a regra global do projeto. Ela obriga qualquer novo extrator a ter um método chamado execute().
# Objetivo: Garantir que todas as ferramentas do projeto sigam o mesmo padrão de funcionamento.

from abc import ABC, abstractmethod
from typing import Any


class BaseExtractor(ABC):
    """Interface abstrata para componentes de extração de dados."""

    def __init__(self, config: Any = None):
        self.config = config

    @abstractmethod
    def execute(self) -> Any:
        """Executa o processo principal de extração."""
        pass
