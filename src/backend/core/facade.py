from .action_registry import ActionRegistry
from backend.shared.result import Result
from typing import Any

class Facade:
    def __init__(self, registry: ActionRegistry):
        self._registry = registry

    def execute(self, action: str, payload: dict[str, Any]) -> Result[Any]:
        return self._registry.execute(action, payload)
