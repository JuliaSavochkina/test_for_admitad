from abc import ABC, abstractmethod


class BaseUseCase(ABC):
    @abstractmethod
    def execute(self, data: dict) -> None:
        pass
