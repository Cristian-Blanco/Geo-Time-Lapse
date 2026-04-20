from qgis.PyQt import QtCore, QtWidgets
from qgis.PyQt.QtGui import QIcon

from frontend.presentation.views.base_page import BasePage

from frontend.config.app import ENABLE_ADVANCED_MODE
from frontend.config.paths import ICONS_DIR
from frontend.store.wizard_context import WizardContext
from frontend.domain.wizard.types import Mode

class ModePage(BasePage):
    left_mode = "previous"
    right_mode = "next"

    def __init__(self, widget: QtWidgets.QWidget, state: WizardContext):
        super().__init__(widget, state)

        self.title = self.tr("Select configuration")
        self.description = self.tr("What type of configuration would you like to select?")

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

        self._apply_static_assets()
        self._apply_selected_styles()
        self.validityChanged.emit(self.is_valid())
        self.stateChanged.emit()

    def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
            if obj is self.card_basic:
                self._select("basic")
                return True
            if obj is self.card_advanced and ENABLE_ADVANCED_MODE:
                self._select("advanced")
                return True
        return bool(super().eventFilter(obj, event))

    def _select(self, mode: Mode) -> None:
        if self.state.mode == mode:
            return
        self.state.mode = mode
        self._apply_selected_styles()
        self.validityChanged.emit(self.is_valid())
        self.stateChanged.emit()

    def _apply_selected_styles(self) -> None:
        desired = {
            self.card_basic: self.state.mode == "basic",
            self.card_advanced: self.state.mode == "advanced",
        }

        for w, selected in desired.items():
            if w.property("selected") == selected:
                continue

            w.setProperty("selected", selected)

            st = w.style()
            st.unpolish(w)
            st.polish(w)
            w.update()

    def is_valid(self) -> bool:
        if ENABLE_ADVANCED_MODE:
            return self.state.mode in ("basic", "advanced")
        return self.state.mode == "basic"

    def _apply_static_assets(self) -> None:
        assets = { #Dynamic content
            True: {
                "icon": "advanced.png",
                "text": self.tr("For users with GIS experience."),
            },
            False: {
                "icon": "construction.png",
                "text": self.tr("Under construction"),
            },
        }

        basic_png = str(ICONS_DIR / "basic.png")
        adv_cfg = assets[bool(ENABLE_ADVANCED_MODE)]

        # Basic icon
        if img_basic := self.widget.findChild(QtWidgets.QLabel, "img_basic"):
            img_basic.setPixmap(QIcon(basic_png).pixmap(90, 90))

        # Advanced icon
        if img_adv := self.widget.findChild(QtWidgets.QLabel, "img_advanced"):
            img_adv.setPixmap(QIcon(str(ICONS_DIR / adv_cfg["icon"])).pixmap(90, 90))

        # Advanced description
        if lbl_adv_desc := self.widget.findChild(QtWidgets.QLabel, "lbl_adv_desc"):
            lbl_adv_desc.setText(adv_cfg["text"])
