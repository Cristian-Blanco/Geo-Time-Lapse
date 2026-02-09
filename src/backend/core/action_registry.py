from backend.contracts.action import Action
from backend.shared.result import Result
from typing import Any

class ActionRegistry:
    def __init__(self) -> None:
        self._actions: dict[str, Action[Any, Any]] = {}

    def register(self, name: str, action: Action[Any, Any]) -> None:
        if name in self._actions:
            raise RuntimeError(f"Action already registered: {name}")
        self._actions[name] = action

    def execute(self, name: str, payload: dict[str, Any]) -> Result[Any]:
        action = self._actions.get(name)
        if not action:
            return Result.fail(f"Unknown action: {name}")
        return action.invoke(payload)
