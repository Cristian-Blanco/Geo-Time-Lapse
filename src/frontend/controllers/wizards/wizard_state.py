from dataclasses import dataclass
from typing import Optional
from frontend.config.wizard_flow import MODE

@dataclass
class WizardState:
    project_id: str = ""
    authenticated: bool = False
    mode: Optional[MODE] = None
