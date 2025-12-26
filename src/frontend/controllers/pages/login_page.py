from qgis.PyQt import QtWidgets
from frontend.controllers.pages.base_page import BasePage
from qgis.PyQt import QtCore
from qgis.PyQt.QtGui import QIcon
from frontend.config.paths import ICONS_DIR

class LoginPage(BasePage):
    left_mode = "cancel"
    right_mode = "next"

    def __init__(self, widget: QtWidgets.QWidget, state):
        super().__init__(widget, state)

        self.title = self.tr("Conéctate a Google Earth Engine")
        self.description = self.tr("Por favor ingresa tus credenciales para iniciar sesión.")

        self.inp_project_id: QtWidgets.QLineEdit = widget.findChild(QtWidgets.QLineEdit, "inp_project_id")
        self.btn_sign_in: QtWidgets.QPushButton = widget.findChild(QtWidgets.QPushButton, "btn_sign_in")
        self.btn_verify: QtWidgets.QPushButton = widget.findChild(QtWidgets.QPushButton, "btn_verify")
        self.lbl_auth_status: QtWidgets.QLabel = widget.findChild(QtWidgets.QLabel, "lbl_auth_status")

        if not all([self.inp_project_id, self.btn_sign_in, self.btn_verify, self.lbl_auth_status]):
            raise RuntimeError(
                "wizard_01_login.ui: missing objectName (inp_project_id, btn_sign_in, btn_verify, lbl_auth_status)"
            )

        # Load assets
        self.__apply_static_assets()

        self.inp_project_id.textChanged.connect(self._on_project_id_changed)
        self.btn_sign_in.clicked.connect(self._on_sign_in_clicked)
        self.btn_verify.clicked.connect(self._on_verify_clicked)

        self._render()

    def _on_project_id_changed(self, txt: str) -> None:
        self.state.project_id = (txt or "").strip()
        self._render()

    def _on_sign_in_clicked(self) -> None:
        # MVP: simulación
        self.state.authenticated = True
        self._render()

    def _on_verify_clicked(self) -> None:
        self.state.verified = bool(self.state.project_id) and bool(self.state.authenticated)
        self._render()

    def _render(self) -> None:
        if getattr(self.state, "verified", False):
            self.lbl_auth_status.setText(self.tr("✅ Verificado"))
        elif self.state.authenticated:
            self.lbl_auth_status.setText(self.tr("🔓 Autenticado (falta verificar)"))
        else:
            self.lbl_auth_status.setText(self.tr("🔒 No autenticado"))

        self.validityChanged.emit(self.is_valid())
        self.stateChanged.emit()

    def is_valid(self) -> bool:
        return bool(self.state.project_id) and bool(getattr(self.state, "verified", False))

    def __apply_static_assets(self) -> None:
        # Load assets without qrc
        google_png = str(ICONS_DIR / "google_logo.png")
        form_png = str(ICONS_DIR / "exam.png")

        lbl_project_icon = self.widget.findChild(QtWidgets.QLabel, "lbl_project_icon")
        if lbl_project_icon:
            lbl_project_icon.setPixmap(QIcon(form_png).pixmap(16, 16))

        self.btn_sign_in.setIcon(QIcon(google_png))
        self.btn_sign_in.setIconSize(QtCore.QSize(18, 18))
