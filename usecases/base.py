from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def execute(self):
        pass
