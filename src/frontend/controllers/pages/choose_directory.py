from frontend.controllers.pages.base_page import BasePage
from frontend.controllers.wizards.wizard_state import WizardState
from qgis.PyQt import QtWidgets, QtCore
from qgis.PyQt.QtGui import QIcon
from frontend.config.paths import ICONS_DIR


class ChooseDirectory(BasePage):
    left_mode = "previous"
    right_mode = "next"

    def __init__(self, widget: QtWidgets.QWidget, state: WizardState) -> None:
        super().__init__(widget, state)

        self.title = self.tr("Choose Directory")
        self.description = self.tr("Select where the output video will be saved")

        self.input_directory: QtWidgets.QLineEdit = widget.findChild(
            QtWidgets.QLineEdit, "input_directory"
        )
        self.btn_browse: QtWidgets.QToolButton = widget.findChild(
            QtWidgets.QToolButton, "btn_browse"
        )

        if not self.input_directory or not self.btn_browse:
            raise RuntimeError("wizard_05_choose_directory.ui: missing widgets")

        self.btn_browse.setIcon(QIcon(str(ICONS_DIR / "folder.png")))
        self.btn_browse.setIconSize(QtCore.QSize(20, 20))
        self.btn_browse.clicked.connect(self._browse_directory)

        # Restore previous state
        if self.state.output_dir:
            self.input_directory.setText(self.state.output_dir)

        self.validityChanged.emit(self.is_valid())

    def _browse_directory(self) -> None:
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self.widget,
            self.tr("Select output directory"),
            self.state.output_dir or ""
        )

        if directory:
            self.state.output_dir = directory
            self.input_directory.setText(directory)
            self.validityChanged.emit(True)
            self.stateChanged.emit()

    def is_valid(self) -> bool:
        return bool(self.state.output_dir)
