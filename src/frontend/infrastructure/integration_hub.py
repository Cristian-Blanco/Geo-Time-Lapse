from backend.bootstrap.action_catalog import ActionCatalog
from backend.core.facade import Facade

class IntegrationHub:
    _instance: "IntegrationHub | None" = None
    _facade: Facade | None

    def __new__(cls) -> "IntegrationHub":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._facade = None
        return cls._instance

    @property
    def facade(self) -> Facade:
        if self._facade is None:
            bootstrap = ActionCatalog()
            self._facade = bootstrap.build_facade()
        return self._facade
