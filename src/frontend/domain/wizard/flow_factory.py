from .flow import Flow
from frontend.domain.wizard.types import (
    WizardBlueprint, WizardNode, NextRule, NextFn, NextTo, NextSwitch, WizardState
    )
from typing import cast

class FlowFactory:
    def __init__(self, blueprint: WizardBlueprint):
        self.blueprint = blueprint

    def build(self) -> Flow:
        start: str = self.blueprint["start"]
        nodes: dict[str, WizardNode] = self.blueprint["nodes"]

        flow: Flow = Flow(start=start)

        for node_id, node_def in nodes.items():
            rule: NextRule = node_def["next"]
            flow.set_next(node_id, self._compile(rule))

        return flow

    def _compile(self, rule: NextRule) -> NextFn:
        type_rule = rule["type"]

        if type_rule == "to":
            rule_to = cast(NextTo, rule)
            target = rule_to["target"]
            return lambda s, _target=target: _target

        if type_rule == "end":
            return lambda s: None

        if type_rule == "switch":
            rule_switch = cast(NextSwitch, rule)
            cases = rule_switch["cases"]
            default = rule_switch["default"]
            switch_on = rule_switch["switch_on"]

            def _fn(state: WizardState) -> str | None:
                raw = getattr(state, switch_on)
                if not isinstance(raw, str):
                    return default
                return cases.get(raw, default)

            return _fn

        raise ValueError(f"Unsupported next type: {type_rule}")
