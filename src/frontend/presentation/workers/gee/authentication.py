from qgis.PyQt.QtCore import QThread, pyqtSignal
from frontend.infrastructure.integration_hub import IntegrationHub

class Authentication(QThread):
    success = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, force: bool = False):
        super().__init__()
        self.force = force

    def run(self) -> None:
        try:
            result = IntegrationHub().facade.execute(
                "gee.ee_authentication",
                {"force": self.force},
            )

            if getattr(result, "ok", False):
                self.success.emit()
            else:
                msg = getattr(result, "error", None)
                self.error.emit(str(msg))

        except Exception as e:
            self.error.emit(str(e))
