from backend.core import Facade, ActionRegistry
from backend.actions.gee.ee_authentication import EEAuthentication
from backend.actions.gee.ee_project_verification import EEProjectVerification
from backend.actions.animation.basic_time_lapse_generation import BasicTimeLapseGeneration

class ActionCatalog:
    def __init__(self) -> None:
        self._registry = ActionRegistry()

    def register_actions(self) -> None:
        self._registry.register("gee.ee_authentication", EEAuthentication())
        self._registry.register("gee.ee_verify_project", EEProjectVerification())
        self._registry.register("generate.basic.timelapse", BasicTimeLapseGeneration())

    def build_facade(self) -> Facade:
        self.register_actions()
        return Facade(self._registry)
