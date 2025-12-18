from __future__ import annotations
from typing import Dict, Optional, Callable
from frontend.controllers.wizards.wizard_state import WizardState

NextFn = Callable[[WizardState], Optional[str]]

class Flow:
    def __init__(self, start: str):
        self.start: str = start
        self._next: Dict[str, NextFn] = {}

    def set_next(self, node_id: str, fn: NextFn) -> None:
        self._next[node_id] = fn

    def next_of(self, node_id: str, state: WizardState) -> Optional[str]:
        fn = self._next.get(node_id)
        return fn(state) if fn else None
