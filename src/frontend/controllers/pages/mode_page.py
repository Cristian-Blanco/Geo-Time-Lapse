from qgis.PyQt import QtWidgets
from frontend.controllers.pages.base_page import BasePage

class ModePage(BasePage):
    title = "Tipo de configuración"
    left_mode = "previous"
    right_mode = "next"

    def __init__(self, widget: QtWidgets.QWidget, state):
        super().__init__(widget, state)

        self.radio_basic: QtWidgets.QRadioButton = widget.findChild(QtWidgets.QRadioButton, "radio_basic")
        self.radio_advanced: QtWidgets.QRadioButton = widget.findChild(QtWidgets.QRadioButton, "radio_advanced")

        if not all([self.radio_basic, self.radio_advanced]):
            raise RuntimeError("wizard_02_mode.ui: missing objectName (radio_basic, radio_advanced)")

        self.radio_basic.toggled.connect(self._on_change)
        self.radio_advanced.toggled.connect(self._on_change)

    def _on_change(self) -> None:
        if self.radio_basic.isChecked():
            self.state.mode = "basic"
        elif self.radio_advanced.isChecked():
            self.state.mode = "advanced"
        else:
            self.state.mode = None

        self.validityChanged.emit(self.is_valid())
        self.stateChanged.emit()

    def is_valid(self) -> bool:
        return self.state.mode in ("basic", "advanced")
