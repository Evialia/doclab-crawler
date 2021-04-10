from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def update(self, entity):
        pass
