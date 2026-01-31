from dataclasses import dataclass
from frontend.domain.wizard.types import Mode, WizardState

@dataclass
class WizardContext(WizardState):
    project_id: str = ""
    authenticated: bool = False
    mode: Mode | None = None
    template: str | None = None

    output_dir: str | None = None

    verified: bool = False
