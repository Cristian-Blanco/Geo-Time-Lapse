# frontend/presentation/workers/process_wizard.py

from qgis.PyQt.QtCore import QThread, pyqtSignal
from frontend.infrastructure.integration_hub import IntegrationHub
from frontend.store.wizard_context import WizardContext

class ProcessWizard(QThread):
    success = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(int, str)

    def __init__(self, context: WizardContext):
        super().__init__()
        self.context = context

    def run(self) -> None:
        try:
            result = IntegrationHub().facade.execute(
                "wizard.process",
                {
                    "mode": self.context.mode,
                    "output_dir": self.context.output_dir,
                    "progress_callback": self._report_progress,
                    "is_cancelled": self.isInterruptionRequested,
                }
            )

            if self.isInterruptionRequested():
                return

            if getattr(result, "ok", False):
                self.success.emit()
            else:
                self.error.emit(str(getattr(result, "error", "Unknown error")))

        except Exception as e:
            self.error.emit(str(e))

    def _report_progress(self, percent: int, message: str) -> None:
        self.progress.emit(percent, message)
