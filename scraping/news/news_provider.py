from abc import ABC, abstractmethod
from typing import Iterable


class NewsProvider(ABC):
    news: dict[str, str]
    
    @abstractmethod
    def __init__(self, searchs: Iterable, *args):
        pass

    @abstractmethod
    def update_values(self) -> dict[str, dict]:
        pass