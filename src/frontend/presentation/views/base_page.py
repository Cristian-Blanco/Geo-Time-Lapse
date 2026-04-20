from __future__ import annotations
from qgis.PyQt import QtCore, QtWidgets
from frontend.store.wizard_context import WizardContext

class BasePage(QtCore.QObject):
    # Emitted when page validity changes (enables/disables navigation)
    validityChanged = QtCore.pyqtSignal(bool)
    # Emitted when shared state changes
    stateChanged = QtCore.pyqtSignal()

    left_mode: str = "previous"
    right_mode: str = "next"

    title: str = ""
    description: str = ""

    cancel_delay_ms: int = 0

    def __init__(self, widget: QtWidgets.QWidget, state: WizardContext):
        super().__init__()
        self.widget = widget
        self.state = state

    # ---------- Lifecycle ----------
    def on_enter(self) -> None:

        self.validityChanged.emit(self.is_valid())

    def on_leave(self) -> None:
        pass

    def is_valid(self) -> bool:
        return True
