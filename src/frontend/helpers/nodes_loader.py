import os
from qgis.PyQt import uic, QtWidgets

from frontend.helpers.controller_resolver import ControllerResolver

class NodesLoader:
    def __init__(self, ui_dir: str, stacked_pages: QtWidgets.QStackedWidget, state, blueprint: dict):
        self.ui_dir = ui_dir
        self.stacked_pages = stacked_pages
        self.state = state
        self.blueprint = blueprint

    def load(self, on_validity, on_state_changed):
        nodes = {}

        for node_id, node_def in self.blueprint["nodes"].items():
            w = self._load_ui(node_def["ui"])
            controller_cls = ControllerResolver.resolve(node_def["controller"])
            page = controller_cls(w, self.state)

            page.validityChanged.connect(on_validity)
            page.stateChanged.connect(on_state_changed)

            nodes[node_id] = (w, page)
            self.stacked_pages.addWidget(w)

        return nodes

    def _load_ui(self, filename: str) -> QtWidgets.QWidget:
        path = os.path.join(self.ui_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"There is no UI: {path}")
        w = QtWidgets.QWidget()
        uic.loadUi(path, w)
        return w
