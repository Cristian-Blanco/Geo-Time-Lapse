from frontend.presentation.views.base_page import BasePage
from frontend.store.wizard_context import WizardContext
from qgis.PyQt import QtWidgets, QtCore
from qgis.PyQt.QtGui import QIcon
from frontend.config.paths import ICONS_DIR

class BasicTimeLapse(BasePage):
    left_mode = "previous"
    right_mode = "next"

    def __init__(self, widget: QtWidgets.QWidget, state: WizardContext) -> None:
        super().__init__(widget, state)

        self.title = self.tr("Time period")
        self.description = self.tr("Select the range for the timelapse")

        self.__apply_child_assets()

    def __apply_child_assets(self) -> None:
        icon_map = {
            "icon_filter": "radar.png",
            "icon_satellite": "satellite.png",
            "icon_cloud": "cloud.png",
        }

        for obj_name, icon_file in icon_map.items():
            btn = self.widget.findChild(QtWidgets.QToolButton, obj_name)
            if btn:
                btn.setIcon(QIcon(str(ICONS_DIR / icon_file)))
                btn.setIconSize(QtCore.QSize(24, 24))
