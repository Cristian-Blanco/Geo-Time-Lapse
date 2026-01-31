import os
from typing import TYPE_CHECKING

from qgis.PyQt import uic, QtWidgets
from frontend.config.paths import UI_DIR, ICONS_DIR

from frontend.store.wizard_context import WizardContext
from frontend.bootstrap.nodes_loader import NodesLoader
from frontend.presentation.structure.wizard_blueprint import WIZARD_BLUEPRINT
from frontend.domain.wizard.flow_factory import FlowFactory
from frontend.domain.wizard.progress_calc import ProgressCalc
from frontend.bootstrap.style_bootstrap import StyleBootstrap
from qgis.PyQt.QtGui import QIcon

if TYPE_CHECKING:
    from frontend.presentation.views.base_page import BasePage

# FORM_CLASS, _ = uic.loadUiType(os.path.join(UI_DIR, "main_dialog.ui"))


# class GeoTimeLapseDialog(QtWidgets.QDialog, FORM_CLASS):
class GeoTimeLapseDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        # Change in the future, with a .env, mode dev and mode production
        # self.setupUi(self)
        ui_path = os.path.join(UI_DIR, "main_dialog.ui")
        uic.loadUi(ui_path, self)

        # Load QSS
        StyleBootstrap.apply(self)

        # Header refs
        self._hdr_title = self.findChild(QtWidgets.QLabel, "dlg_lbl_header_title")
        self._hdr_subtitle = self.findChild(QtWidgets.QLabel, "dlg_lbl_header_subtitle")
        self._hdr_icon = self.findChild(QtWidgets.QLabel, "dlg_lbl_icon_plugin")

        # Icon fijo del plugin (una sola vez)
        self._apply_header_icon()

        # Load Wizard state and wizards
        self.state = WizardContext()
        self.flow = FlowFactory(WIZARD_BLUEPRINT).build()
        self.progress = ProgressCalc(WIZARD_BLUEPRINT)

        # node_id in dict is iqual to (widget, view)
        self._nodes: dict[str, tuple[QtWidgets.QWidget, BasePage]] = {}
        self.min_history_to_go_back = 2
        self._history: list[str] = []
        self._current: str | None = None

        loader = NodesLoader(UI_DIR, self.stacked_pages, self.state, WIZARD_BLUEPRINT)
        self._nodes = loader.load(self._apply_footer_state, self._on_state_changed)

        self._wire_footer()
        self._go_to(self.flow.start, push_history=False)

    def _apply_header_icon(self) -> None:
        if not self._hdr_icon:
            return
        icon_png = str(ICONS_DIR / "icon.png")
        self._hdr_icon.setPixmap(QIcon(icon_png).pixmap(50, 50))

    def _apply_header(self, page: "BasePage") -> None:
        if self._hdr_title:
            self._hdr_title.setText(page.title or "")
        if self._hdr_subtitle:
            self._hdr_subtitle.setText(page.description or "")

    def _wire_footer(self) -> None:
        self.btn_previous.clicked.connect(self._on_left)
        self.btn_next.clicked.connect(self._on_right)

    # ---------- navigation ----------
    def _on_left(self) -> None:
        if not self._current:
            return

        _, page = self._nodes[self._current]
        if page.left_mode == "cancel":
            self.reject()
            return

        if len(self._history) >= self.min_history_to_go_back:
            self._history.pop()
            prev_id = self._history[-1]
            self._go_to(prev_id, push_history=False)

    def _on_right(self) -> None:
        if not self._current:
            return

        _, page = self._nodes[self._current]
        if not page.is_valid():
            return

        if page.right_mode == "finish":
            self.accept()
            return

        nxt = self.flow.next_of(self._current, self.state)
        if nxt is None:
            self.accept()
            return

        self._go_to(nxt, push_history=True)

    def _go_to(self, node_id: str, push_history: bool) -> None:
        self._current = node_id
        w, page = self._nodes[node_id]
        self.stacked_pages.setCurrentWidget(w)

        if push_history:
            self._history.append(node_id)
        elif not self._history:
            self._history.append(node_id)

        # Header changes
        self._apply_header(page)

        page.on_enter()
        self._apply_footer_state(page.is_valid())
        self._apply_progress()

    # ---------- footer + progress ----------
    def _apply_footer_state(self, is_valid: bool) -> None:
        if not self._current:
            return

        _, page = self._nodes[self._current]

        self.btn_previous.setText(self.tr("Cancelar") if page.left_mode == "cancel" else self.tr("Anterior"))
        self.btn_next.setText(self.tr("Terminar") if page.right_mode == "finish" else self.tr("Siguiente"))
        self.btn_previous.setEnabled(len(self._history) > 1 or page.left_mode == "cancel")
        self.btn_next.setEnabled(is_valid)

    def _apply_progress(self) -> None:
        if hasattr(self, "progress_bar"):
            self.progress_bar.setValue(self.progress.percent_for(self._current))

    def _on_state_changed(self) -> None:
        self._apply_progress()
