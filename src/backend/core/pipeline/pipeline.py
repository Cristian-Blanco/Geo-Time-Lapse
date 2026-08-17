from .pipeline_handler import PipelineHandler

from typing import Generic, TypeVar

TContext = TypeVar("TContext")


class Pipeline(Generic[TContext]):

    def __init__(
        self,
        handler: PipelineHandler[TContext] | None = None,
    ):
        self.handlers: list[PipelineHandler[TContext]] = []

        if handler:
            self.handlers.append(handler)

    def add_handler(
        self,
        handler: PipelineHandler[TContext],
    ) -> "Pipeline[TContext]":

        self.handlers.append(handler)
        return self

    def execute(self, context: TContext) -> TContext:

        for handler in self.handlers:
            context = handler.handle(context)

        return context
