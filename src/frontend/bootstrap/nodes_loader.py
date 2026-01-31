from pathlib import Path
from typing import Any
from collections.abc import Callable

from qgis.PyQt import uic, QtWidgets

from frontend.bootstrap.view_resolver import ViewResolver
from frontend.domain.wizard.types import WizardBlueprint


class NodesLoader:
    def __init__(
        self,
        ui_dir: Path,
        stacked_pages: QtWidgets.QStackedWidget,
        state: Any,
        blueprint: WizardBlueprint,
    ) -> None:
        self.ui_dir = ui_dir
        self.stacked_pages = stacked_pages
        self.state = state
        self.blueprint = blueprint

    def load(
        self,
        on_validity: Callable[[bool], None],
        on_state_changed: Callable[[], None],
    ) -> dict[str, tuple[QtWidgets.QWidget, Any]]:
        nodes: dict[str, tuple[QtWidgets.QWidget, Any]] = {}

        for node_id, node_def in self.blueprint["nodes"].items():
            w = self._load_ui(node_def["ui"])

            view_cls = ViewResolver.resolve(node_def["view"])
            page = view_cls(w, self.state)

            page.validityChanged.connect(on_validity)
            page.stateChanged.connect(on_state_changed)

            nodes[node_id] = (w, page)
            self.stacked_pages.addWidget(w)

        return nodes

    def _load_ui(self, filename: str) -> QtWidgets.QWidget:
        path = self.ui_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"There is no UI: {path}")

        w = QtWidgets.QWidget()
        uic.loadUi(str(path), w)
        return w
