from qgis.PyQt import QtWidgets
from frontend.controllers.pages.base_page import BasePage

class LoginPage(BasePage):
    title = "Login Google"
    left_mode = "cancel"
    right_mode = "next"

    def __init__(self, widget: QtWidgets.QWidget, state):
        super().__init__(widget, state)

        self.inp_project_id: QtWidgets.QLineEdit = widget.findChild(QtWidgets.QLineEdit, "inp_project_id")
        self.btn_sign_in: QtWidgets.QPushButton = widget.findChild(QtWidgets.QPushButton, "btn_sign_in")
        self.lbl_auth_status: QtWidgets.QLabel = widget.findChild(QtWidgets.QLabel, "lbl_auth_status")

        if not all([self.inp_project_id, self.btn_sign_in, self.lbl_auth_status]):
            raise RuntimeError("wizard_01_login.ui: missing objectName (inp_project_id, btn_sign_in, lbl_auth_status)")

        self.inp_project_id.textChanged.connect(self._on_project_id_changed)
        self.btn_sign_in.clicked.connect(self._on_sign_in_clicked)

        self._render()

    def _on_project_id_changed(self, txt: str) -> None:
        self.state.project_id = (txt or "").strip()
        self._render()

    def _on_sign_in_clicked(self) -> None:
        self.state.authenticated = True
        self._render()

    def _render(self) -> None:
        if self.state.authenticated:
            self.lbl_auth_status.setText("✅ Authenticated")
        else:
            self.lbl_auth_status.setText("🔒 Not Authenticated")

        self.validityChanged.emit(self.is_valid())
        self.stateChanged.emit()

    def is_valid(self) -> bool:
        return bool(self.state.project_id) and bool(self.state.authenticated)
