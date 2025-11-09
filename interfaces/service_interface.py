from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel

class ServiceInterface(ABC):
    @abstractmethod
    def get_all(self) -> List[BaseModel]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> BaseModel:
        pass

    @abstractmethod
    def create(self, resource_data: BaseModel) -> BaseModel:
        pass

    @abstractmethod
    def update(self, id: str, resource_data: BaseModel) -> BaseModel:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass