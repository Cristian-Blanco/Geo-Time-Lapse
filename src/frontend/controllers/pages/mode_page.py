from qgis.PyQt import QtCore, QtWidgets
from qgis.PyQt.QtGui import QIcon

from frontend.controllers.pages.base_page import BasePage

from frontend.config.wizard_flow import ENABLE_ADVANCED_MODE
from frontend.config.paths import ICONS_DIR

class ModePage(BasePage):
    title = "Seleccionar configuración"
    description = "¿Qué tipo de configuración deseas seleccionar?"

    left_mode = "previous"
    right_mode = "next"

    def __init__(self, widget: QtWidgets.QWidget, state):
        super().__init__(widget, state)
        self.widget = widget

        self.card_basic: QtWidgets.QFrame = widget.findChild(QtWidgets.QFrame, "card_basic")
        self.card_advanced: QtWidgets.QFrame = widget.findChild(QtWidgets.QFrame, "card_advanced")

        if not all([self.card_basic, self.card_advanced]):
            raise RuntimeError("wizard_02_mode.ui: missing objectName (card_basic, card_advanced)")

        # MVP: disabled avanced flow
        self.card_advanced.setEnabled(bool(ENABLE_ADVANCED_MODE))

        # click cards
        self.card_basic.setCursor(QtCore.Qt.PointingHandCursor)
        self.card_basic.installEventFilter(self)

        if ENABLE_ADVANCED_MODE:
            self.card_advanced.setCursor(QtCore.Qt.PointingHandCursor)
            self.card_advanced.installEventFilter(self)
        else:
            self.card_advanced.setCursor(QtCore.Qt.ForbiddenCursor)

        # Default
        if self.state.mode not in ("basic", "advanced"):
            self.state.mode = "basic"

        self.__apply_static_assets()
        self._apply_selected_styles()
        self.validityChanged.emit(self.is_valid())
        self.stateChanged.emit()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
            if obj is self.card_basic:
                self._select("basic")
                return True
            if obj is self.card_advanced and ENABLE_ADVANCED_MODE:
                self._select("advanced")
                return True
        return super().eventFilter(obj, event)

    def _select(self, mode: str) -> None:
        self.state.mode = mode
        self._apply_selected_styles()
        self.validityChanged.emit(self.is_valid())
        self.stateChanged.emit()

    def _apply_selected_styles(self) -> None:
        self.card_basic.setProperty("selected", self.state.mode == "basic")
        self.card_advanced.setProperty("selected", self.state.mode == "advanced")

        # Clear styles for cache, remove in the future for production
        for w in (self.card_basic, self.card_advanced):
            w.style().unpolish(w)
            w.style().polish(w)
            w.update()

    def is_valid(self) -> bool:
        if ENABLE_ADVANCED_MODE:
            return self.state.mode in ("basic", "advanced")
        return self.state.mode == "basic"

    def __apply_static_assets(self) -> None:
        basic_png = str(ICONS_DIR / "basic.png")
        advanced_png = str(ICONS_DIR / ("advanced.png" if ENABLE_ADVANCED_MODE else "construction.png"))

        img_basic = self.widget.findChild(QtWidgets.QLabel, "img_basic")
        if img_basic:
            img_basic.setPixmap(QIcon(basic_png).pixmap(90, 90))

        img_adv = self.widget.findChild(QtWidgets.QLabel, "img_advanced")
        if img_adv:
            img_adv.setPixmap(QIcon(advanced_png).pixmap(90, 90))
