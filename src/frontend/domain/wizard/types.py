from typing import TypedDict, Literal, TypeAlias, Protocol
from collections.abc import Callable

class NextTo(TypedDict):
    type: Literal["to"]
    target: str


class NextEnd(TypedDict):
    type: Literal["end"]


class NextSwitch(TypedDict):
    type: Literal["switch"]
    cases: dict[str, str]
    default: str | None
    switch_on: str


NextRule = NextTo | NextEnd | NextSwitch


class WizardNode(TypedDict):
    ui: str
    view: str
    next: NextRule
    step: int


class WizardBlueprint(TypedDict):
    start: str
    total_steps: int
    nodes: dict[str, WizardNode]


Mode: TypeAlias = Literal["basic", "advanced"]


class WizardState(Protocol):
    ...


NextFn: TypeAlias = Callable[[WizardState], str | None]
