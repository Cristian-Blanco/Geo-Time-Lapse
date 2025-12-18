from .flow import Flow

class FlowFactory:
    def __init__(self, blueprint: dict):
        self.blueprint = blueprint

    def build(self) -> Flow:
        start: str = self.blueprint["start"]
        nodes: dict = self.blueprint["nodes"]

        flow: Flow = Flow(start=start)

        for node_id, node_def in nodes.items():
            rule: dict = node_def["next"]
            flow.set_next(node_id, self._compile(rule))

        return flow

    def _compile(self, rule: dict):
        type_rule = rule["type"]

        if type_rule == "to":
            target = rule["target"]
            return lambda s, _target=target: _target

        if type_rule == "end":
            return lambda s: None

        if type_rule == "switch":
            cases = rule["cases"]
            default = rule.get("default")
            switch_on = rule.get("switch_on", "mode")

            def _fn(state):
                key = getattr(state, switch_on, None)
                return cases.get(key, default)
            return _fn

        raise ValueError(f"Unsupported next type: {type_rule}")
