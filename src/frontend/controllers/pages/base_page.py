from __future__ import annotations
from qgis.PyQt import QtCore, QtWidgets
from frontend.controllers.wizards.wizard_state import WizardState

class BasePage(QtCore.QObject):
    validityChanged = QtCore.pyqtSignal(bool)
    stateChanged = QtCore.pyqtSignal()

    left_mode: str = "previous"
    right_mode: str = "next"

    title: str = ""
    description: str = ""

    def __init__(self, widget: QtWidgets.QWidget, state: WizardState):
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
