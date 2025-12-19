class ProgressCalc:
    def __init__(self, blueprint: dict):
        self.total = int(blueprint.get("total_steps", 1))
        self.nodes = blueprint["nodes"]
        self.start = blueprint["start"]

    def percent_for(self, node_id: str | None) -> int:
        nid = node_id or self.start
        step = int(self.nodes.get(nid, {}).get("step", 1))
        return int(step / self.total * 100)
