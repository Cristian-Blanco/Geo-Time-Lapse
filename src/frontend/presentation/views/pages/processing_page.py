from frontend.presentation.views.base_page import BasePage
from frontend.store.wizard_context import WizardContext
from frontend.presentation.workers.generate_timelapse import GenerateTimelapse
from frontend.presentation.workers.orbit_loader import OrbitLoader
from qgis.PyQt import QtWidgets

class ProcessingPage(BasePage):

    left_mode = "cancel"
    right_mode = "finish"

    def __init__(self, widget: QtWidgets.QWidget, state: WizardContext) -> None:
        super().__init__(widget, state)

        self.title = self.tr("Processing")
        self.description = self.tr("Generating animation")

        self.process_completed = False
        self.worker: GenerateTimelapse | None = None

        self.lbl_percentage = self.widget.findChild(QtWidgets.QLabel, "lbl_percentage")
        self.lbl_status = self.widget.findChild(QtWidgets.QLabel, "lbl_status")
        self.loader_circle = self.widget.findChild(QtWidgets.QWidget, "loader_circle")
        self.success_card = self.widget.findChild(QtWidgets.QFrame, "success_card")
        self.lbl_success_title = self.widget.findChild(QtWidgets.QFrame, "lbl_success_title")

        self.orbit = OrbitLoader(self.loader_circle)
        self.orbit.setGeometry(self.loader_circle.rect())
        self.orbit.lower()
        self.orbit.show()

    def _on_progress(self, percent: int, message: str) -> None:
        self.lbl_percentage.setText(f"{percent}%")
        self.lbl_status.setText(self.tr(message))

    def on_enter(self) -> None:
        self._reset_loading_state()

        self.worker = GenerateTimelapse(self.state)
        self.worker.success.connect(self._on_success)
        self.worker.error.connect(self._on_error)
        self.worker.progress.connect(self._on_progress)

        self.worker.start()

    def _reset_loading_state(self) -> None:
        self.process_completed = False

        self.lbl_percentage.setText("0%")
        self.lbl_status.setText(self.tr("Loading..."))

        self.success_card.hide()
        self.loader_circle.show()
        self.orbit.show()
        self.orbit.raise_()

    def _on_success(self, video_path: str) -> None:
        if hasattr(self, "orbit"):
            self.orbit.hide()

        self.loader_circle.hide()
        self.success_card.show()

        message = self.tr("Export completed successfully.")
        path_label = self.tr("Saved at:")

        self.lbl_success_title.setText(
            f"{message}\n{path_label}\n{video_path}"
        )

        self.process_completed = True
        self.validityChanged.emit(self.is_valid())

    def is_valid(self) -> bool:
        return self.process_completed

    def on_leave(self) -> None:
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
            self.worker.wait(3000)

        self.worker = None

    def _on_error(self, message: str) -> None:
        self.lbl_status.setText(self.tr("Error during processing"))
        if hasattr(self, "orbit"):
            self.orbit.hide()

        QtWidgets.QMessageBox.critical(
            self.widget,
            "Error",
            message
        )
