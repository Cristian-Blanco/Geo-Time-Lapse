from frontend.domain.wizard.types import WizardBlueprint

class ProgressCalc:
    def __init__(self, blueprint: WizardBlueprint):
        self.total = int(blueprint.get("total_steps", 1))
        self.nodes = blueprint["nodes"]
        self.start = blueprint["start"]

    def percent_for(self, node_id: str | None) -> int:
        nid = node_id or self.start
        node = self.nodes.get(nid)

        if not node:
            return 0

        step = node["step"]
        return int(step / self.total * 100)
