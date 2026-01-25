from dataclasses import dataclass
from frontend.config.wizard_flow import MODE

@dataclass
class WizardState:
    project_id: str = ""
    authenticated: bool = False
    mode: MODE | None = None
    template: str | None = None

    verified: bool = False
