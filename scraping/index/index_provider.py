from abc import ABC, abstractmethod
from typing import Iterable


class IndexProvider(ABC):
    indexes: dict[str, float]
    
    @abstractmethod
    def __init__(self, searchs: Iterable, *args):
        pass

    @abstractmethod
    def update_values(self) -> dict[str, float]:
        pass