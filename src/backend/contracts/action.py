from abc import ABC, abstractmethod
from backend.shared.result import Result
from typing import TypeVar, Generic

T = TypeVar("T")
P = TypeVar("P")

class Action(ABC, Generic[P, T]):

    @abstractmethod
    def invoke(self, payload: P) -> Result[T]:
        pass
