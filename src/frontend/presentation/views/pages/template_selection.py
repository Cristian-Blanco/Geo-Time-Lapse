from frontend.presentation.views.base_page import BasePage
from frontend.store.wizard_context import WizardContext
from qgis.PyQt import QtWidgets, QtCore
from qgis.PyQt.QtGui import QIcon
from frontend.presentation.data.templates import TEMPLATES
from frontend.domain.templates.types import TemplateDefItem

class TemplateSelection(BasePage):
    left_mode = "previous"
    right_mode = "next"

    def __init__(self, widget: QtWidgets.QWidget, state: WizardContext) -> None:
        super().__init__(widget, state)

        self.title = self.tr("Choose Template")
        self.description = self.tr("Select how the timelapse will be displayed")

        self._load_templates()

    def _create_template_card(self, tpl: TemplateDefItem) -> QtWidgets.QFrame:
        card = QtWidgets.QFrame()
        card.setObjectName(f"card_{tpl['id']}")
        card.setProperty("template_id", tpl["id"])
        card.setProperty("selected", False)
        card.setProperty("class", "card_group")
        card.setEnabled(tpl["enabled"])

        card.setMinimumWidth(190)
        card.setFixedHeight(300)
        card.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )

        card.setCursor(
            QtCore.Qt.PointingHandCursor
            if tpl["enabled"]
            else QtCore.Qt.ForbiddenCursor
        )

        layout = QtWidgets.QVBoxLayout(card)
        layout.setSpacing(8)

        lbl_title = QtWidgets.QLabel(self.tr(tpl["title"]))
        lbl_title.setProperty("class", "group_title")
        layout.addWidget(lbl_title, alignment=QtCore.Qt.AlignHCenter)

        lbl_img = QtWidgets.QLabel()
        lbl_img.setAlignment(QtCore.Qt.AlignHCenter)
        lbl_img.setPixmap(QIcon(tpl["icon"]).pixmap(100, 100))
        lbl_img.setProperty("class", "card_image")
        layout.addWidget(lbl_img)

        lbl_desc = QtWidgets.QLabel(self.tr(tpl["description"]))
        lbl_desc.setWordWrap(True)
        lbl_desc.setAlignment(QtCore.Qt.AlignHCenter)
        lbl_desc.setProperty("class", "group_description")
        layout.addWidget(lbl_desc)

        if tpl["enabled"]:
            card.installEventFilter(self)

        return card

    def _load_templates(self) -> None:
        grid: QtWidgets.QGridLayout = self.widget.findChild(
            QtWidgets.QGridLayout, "cards_grid"
        )

        for i, tpl in enumerate(TEMPLATES):
            row = i // 3
            col = i % 3
            card = self._create_template_card(tpl)
            grid.addWidget(card, row, col)

        grid.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        for col in range(3):
            grid.setColumnStretch(col, 1)

    def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if (
            event.type() == QtCore.QEvent.MouseButtonRelease
            and isinstance(obj, QtWidgets.QFrame)
            and obj.isEnabled()
        ):
            self._select_template(obj.property("template_id"))
            return True

        return False

    def _select_template(self, template_id: str) -> None:
        self.state.template = template_id

        for card in self.widget.findChildren(QtWidgets.QFrame):
            if not card.objectName().startswith("card_"):
                continue

            selected = card.property("template_id") == template_id
            card.setProperty("selected", selected)

            st = card.style()
            st.unpolish(card)
            st.polish(card)
            card.update()

        self.validityChanged.emit(True)
        self.stateChanged.emit()

    def is_valid(self) -> bool:
        return self.state.template is not None
