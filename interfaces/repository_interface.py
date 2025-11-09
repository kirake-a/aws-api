from abc import ABC, abstractmethod


class RepositoryInterface(ABC):
    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def get(self, item_id):
        pass

    @abstractmethod
    def update(self, item_id, item):
        pass

    @abstractmethod
    def delete(self, item_id):
        pass

    @abstractmethod
    def list(self):
        pass