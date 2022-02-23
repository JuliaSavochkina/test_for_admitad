from abc import ABC, abstractmethod
from typing import Optional


class BaseUseCase(ABC):
    """
    Абстрактный класс для всех юзкейсов
    """
    @abstractmethod
    def execute(self, data: dict) -> Optional[dict]:
        pass
