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
                    "project_id": self.context.project_id,
                    "template": self.context.template,
                    "output_dir": self.context.output_dir,

                    "gallery_id": self.context.gallery_id,
                    "image_type": self.context.image_type,
                    "composition": self.context.composition,
                    "cloud_percentage": self.context.cloud_percentage,

                    "coordinates": self.context.coordinates,

                    "temporal_interval_months": self.context.temporal_interval_months,

                    "start_date": self.context.start_date,
                    "end_date": self.context.end_date,

                    "frame_duration_seconds": self.context.frame_duration_seconds,

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
