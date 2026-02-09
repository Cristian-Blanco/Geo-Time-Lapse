from qgis.PyQt.QtCore import QThread, pyqtSignal
from frontend.infrastructure.integration_hub import IntegrationHub
from qgis.core import QgsMessageLog, Qgis

class VerifyAuth(QThread):
    success = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id

    def run(self) -> None:
        try:
            result = IntegrationHub().facade.execute(
                "gee.ee_verify_project",
                {"project_id": self.project_id},
            )
            QgsMessageLog.logMessage(f"[VerifyAuth] this is result ='{result}'", "GeoTimeLapse", Qgis.Info)

            if getattr(result, "ok", False):
                self.success.emit()
            else:
                msg = getattr(result, "error", None)
                self.error.emit(str(msg))

        except Exception as e:
            self.error.emit(str(e))
