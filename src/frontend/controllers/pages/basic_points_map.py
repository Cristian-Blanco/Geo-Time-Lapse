from frontend.controllers.pages.base_page import BasePage
from frontend.controllers.wizards.wizard_state import WizardState
from qgis.PyQt import QtWidgets, QtCore
from qgis.PyQt.QtGui import QIcon
from frontend.config.paths import ICONS_DIR

class BasicPointsMap(BasePage):
    left_mode = "previous"
    right_mode = "next"

    def __init__(self, widget: QtWidgets.QWidget, state: WizardState) -> None:
        super().__init__(widget, state)

        self.title = self.tr("Video area")
        self.description = self.tr("Define the geographic area that will be used to generate the timelapse.")

        self.__apply_child_assets()
        self.__connect_accordion()

    def __apply_child_assets(self) -> None:
        pin_png = str(ICONS_DIR / "location.png")
        btn = self.widget.findChild(QtWidgets.QPushButton, "btn_select_map")
        if btn:
            btn.setIcon(QIcon(pin_png))
            btn.setIconSize(QtCore.QSize(18, 18))

    def __connect_accordion(self) -> None:
        toggle_btn = self.widget.findChild(QtWidgets.QToolButton, "btn_manual_toggle")
        body = self.widget.findChild(QtWidgets.QWidget, "manual_body")

        if not toggle_btn or not body:
            return

        body.setVisible(toggle_btn.isChecked())
        self.__update_arrow(toggle_btn)

        toggle_btn.toggled.connect(lambda checked: self.__toggle_manual_body(checked, body, toggle_btn))

    def __toggle_manual_body(
        self,
        checked: bool,
        body: QtWidgets.QWidget,
        btn: QtWidgets.QToolButton,
    ) -> None:
        body.setVisible(checked)
        self.__update_arrow(btn)

    def __update_arrow(self, btn: QtWidgets.QToolButton) -> None:
        btn.setArrowType(QtCore.Qt.DownArrow if btn.isChecked() else QtCore.Qt.RightArrow)
