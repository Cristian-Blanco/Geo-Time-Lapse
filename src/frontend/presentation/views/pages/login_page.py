from qgis.PyQt import QtWidgets
from frontend.presentation.views.base_page import BasePage
from qgis.PyQt import QtCore
from qgis.PyQt.QtGui import QIcon
from frontend.config.paths import ICONS_DIR
from frontend.store.wizard_context import WizardContext
from frontend.presentation.workers.gee import Authentication, AuthVerification

class LoginPage(BasePage):
    left_mode = "cancel"
    right_mode = "next"

    def __init__(self, widget: QtWidgets.QWidget, state: WizardContext):
        super().__init__(widget, state)

        self.title = self.tr("Connect to Google Earth Engine")
        self.description = self.tr("Enter your credentials to sign in.")

        self.inp_project_id: QtWidgets.QLineEdit = widget.findChild(QtWidgets.QLineEdit, "inp_project_id")
        self.settings = QtCore.QSettings()
        saved_project = self.settings.value("geo_timelapse/gee_project_id", "", type=str)

        if saved_project:
            self.inp_project_id.setText(saved_project)
            self.state.project_id = saved_project
            self.state.authenticated = True

        self.btn_sign_in: QtWidgets.QPushButton = widget.findChild(QtWidgets.QPushButton, "btn_sign_in")
        self.btn_verify: QtWidgets.QPushButton = widget.findChild(QtWidgets.QPushButton, "btn_verify")
        self.lbl_auth_status: QtWidgets.QLabel = widget.findChild(QtWidgets.QLabel, "lbl_auth_status")

        # Load assets
        self._apply_static_assets()

        self.inp_project_id.textChanged.connect(self._on_project_id_changed)
        self.btn_sign_in.clicked.connect(self._on_sign_in_clicked)
        self.btn_verify.clicked.connect(self._on_verify_clicked)

        self._render()

    # ------------------------------------------------------------
    # -------------- AUTH with Google Earth Engine ---------------
    # ------------------------------------------------------------

    def _on_sign_in_clicked(self) -> None:
        self.lbl_auth_status.setText(self.tr("🔄 Authenticating..."))
        self.btn_sign_in.setEnabled(False)

        self.auth_worker = Authentication(True)

        self.auth_worker.success.connect(self._on_auth_success)
        self.auth_worker.error.connect(self._on_auth_error)

        self.auth_worker.start()

    def _on_auth_success(self) -> None:
        self.state.authenticated = True
        self.btn_sign_in.setEnabled(True)
        self._render()

    def _on_auth_error(self, msg: str) -> None:
        self.state.authenticated = False
        self.btn_sign_in.setEnabled(True)
        self.lbl_auth_status.setText(f"🔴 Error: {msg}")

    # ------------------------------------------------------------
    # --------------------- Verify project -----------------------
    # ------------------------------------------------------------

    def _on_verify_clicked(self) -> None:
        if not self.state.project_id:
            self.lbl_auth_status.setText(self.tr("Alert: Enter a Project ID"))
            return

        self.lbl_auth_status.setText(self.tr("Verifying project..."))
        self.btn_verify.setEnabled(False)

        self.verify_worker = AuthVerification(self.state.project_id)

        self.verify_worker.success.connect(self._on_verify_success)
        self.verify_worker.error.connect(self._on_verify_error)

        self.verify_worker.start()

    def _on_verify_success(self) -> None:
        self.state.verified = True
        self.btn_verify.setEnabled(True)

        self.settings.setValue("geo_timelapse/gee_project_id", self.state.project_id)

        self._render()

    def _on_verify_error(self, msg: str) -> None:
        self.state.verified = False
        self.btn_verify.setEnabled(True)

        message_lower = msg.lower()
        if "authenticate" in message_lower or "credentials" in message_lower:
            self.lbl_auth_status.setText(self.tr("🔴 Sign in with Google to continue"))
        else:
            self.lbl_auth_status.setText(f"🔴 {msg}")

    # ------------------------------------------------------------
    # ------------------------ On change -------------------------
    # ------------------------------------------------------------
    def _render(self) -> None:
        if getattr(self.state, "verified", False):
            self.lbl_auth_status.setText(self.tr("🟢 Verified"))
        elif self.state.authenticated:
            self.lbl_auth_status.setText(self.tr("🟠 Authenticated (verification pending)"))
        else:
            self.lbl_auth_status.setText(self.tr("🟠 Not authenticated"))

        self.btn_verify.setEnabled(bool(self.state.project_id))
        self.validityChanged.emit(self.is_valid())
        self.stateChanged.emit()

    def _on_project_id_changed(self, txt: str) -> None:
        self.state.project_id = (txt or "").strip()
        self.state.verified = False
        self._render()

    def is_valid(self) -> bool:
        return bool(self.state.project_id) and bool(getattr(self.state, "verified", False))

    def _apply_static_assets(self) -> None:
        # Load assets without qrc
        google_png = str(ICONS_DIR / "google_logo.png")
        form_png = str(ICONS_DIR / "exam.png")

        lbl_project_icon = self.widget.findChild(QtWidgets.QLabel, "lbl_project_icon")
        if lbl_project_icon:
            lbl_project_icon.setPixmap(QIcon(form_png).pixmap(16, 16))

        self.btn_sign_in.setIcon(QIcon(google_png))
        self.btn_sign_in.setIconSize(QtCore.QSize(18, 18))
