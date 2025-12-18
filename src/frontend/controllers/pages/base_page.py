from __future__ import annotations
from qgis.PyQt import QtCore, QtWidgets
from frontend.controllers.wizards.wizard_state import WizardState

class BasePage(QtCore.QObject):
    validityChanged = QtCore.pyqtSignal(bool)
    stateChanged = QtCore.pyqtSignal()

    # Custom per page
    left_mode: str = "previous"   # "previous" | "cancel"
    right_mode: str = "next"      # "next" | "finish"
    title: str = ""

    def __init__(self, widget: QtWidgets.QWidget, state: WizardState):
        super().__init__()
        self.widget = widget
        self.state = state

    def on_enter(self) -> None:
        self.validityChanged.emit(self.is_valid())

    def on_leave(self) -> None:
        pass

    def is_valid(self) -> bool:
        return True
