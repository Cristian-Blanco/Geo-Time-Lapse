from __future__ import annotations
from .types import NextFn, WizardState

class Flow:
    def __init__(self, start: str):
        self.start: str = start
        self._next: dict[str, NextFn] = {}

    def set_next(self, node_id: str, fn: NextFn) -> None:
        self._next[node_id] = fn

    def next_of(self, node_id: str, state: WizardState) -> str | None:
        fn = self._next.get(node_id)
        return fn(state) if fn else None
