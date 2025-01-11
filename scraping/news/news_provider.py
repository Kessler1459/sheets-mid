from abc import ABC, abstractmethod
from typing import Iterable


class NewsProvider(ABC):
    news: dict[str, dict]

    @abstractmethod
    def __init__(self, searchs: Iterable):
        pass

    @abstractmethod
    def update_values(self) -> dict[str, str]:
        pass