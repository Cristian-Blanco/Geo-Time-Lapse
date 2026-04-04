from backend.core import Facade, ActionRegistry
from backend.actions.gee.ee_authentication import EEAuthentication
from backend.actions.gee.ee_verify_project import EEVerifyProject
from backend.actions.animation.generate_basic_timelapse import GenerateBasicTimelapse

class ActionCatalog:
    def __init__(self) -> None:
        self._registry = ActionRegistry()

    def register_actions(self) -> None:
        self._registry.register("gee.ee_authentication", EEAuthentication())
        self._registry.register("gee.ee_verify_project", EEVerifyProject())
        self._registry.register("generate.basic.timelapse", GenerateBasicTimelapse())

    def build_facade(self) -> Facade:
        self.register_actions()
        return Facade(self._registry)
