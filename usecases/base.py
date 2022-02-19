from abc import ABC, abstractmethod
from typing import Optional


class BaseUseCase(ABC):
    @abstractmethod
    def execute(self, data: dict) -> Optional[dict]:
        pass
