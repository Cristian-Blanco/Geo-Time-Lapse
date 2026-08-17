from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TContext = TypeVar("TContext")

class PipelineHandler(ABC, Generic[TContext]):

    @abstractmethod
    def handle(self, context: TContext) -> TContext:
        pass
