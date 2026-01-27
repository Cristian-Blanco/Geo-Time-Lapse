from qgis.PyQt import QtWidgets, QtCore, QtGui
from frontend.controllers.pages.base_page import BasePage
from frontend.controllers.wizards.wizard_state import WizardState
from frontend.config.satellite import (
    IMAGE_TYPES,
    IMAGE_GALLERIES,
    IMAGE_COMPOSITIONS,
)
from frontend.config.paths import ICONS_DIR
from typing import Any

class BasicImageType(BasePage):
    left_mode = "previous"
    right_mode = "next"

    def __init__(self, widget: QtWidgets.QWidget, state: WizardState) -> None:
        super().__init__(widget, state)

        self.title: str = self.tr("Image type")
        self.description: str = self.tr(
            "Select the type of satellite image to be used to generate the timelapse."
        )

        self.selected_image_type: str | None = None
        self.image_cards: dict[str, QtWidgets.QFrame] = {}

        self.widget.when_to_use_panel.setFixedWidth(280)
        self.widget.when_to_use_panel.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Expanding
        )

        self.widget.cloud_slider.valueChanged.connect(self._update_cloud_label)
        self._update_cloud_label(self.widget.cloud_slider.value())

        self._load_image_types()
        self._load_extras()
        self._setup_accordion()

    # -------------------------
    # Image cards
    # -------------------------
    def _load_image_types(self) -> None:
        for item in IMAGE_TYPES:
            card = self._create_image_card(item)
            self.image_cards[item["id"]] = card
            self.widget.image_type_list.addWidget(card)

    def _create_image_card(self, item: dict[str, Any]) -> QtWidgets.QFrame:
        card = QtWidgets.QFrame()
        card.setObjectName("image_type_card")
        card.setProperty("selected", False)
        card.setCursor(QtCore.Qt.PointingHandCursor)

        card.setFixedHeight(76)
        card.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )

        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(12)

        img = QtWidgets.QLabel()
        img.setFixedSize(54, 54)
        img.setScaledContents(True)
        img.setPixmap(QtGui.QPixmap(str(ICONS_DIR / item["icon"])))

        text_layout = QtWidgets.QVBoxLayout()
        text_layout.setSpacing(2)
        text_layout.setAlignment(QtCore.Qt.AlignTop)

        title = QtWidgets.QLabel(item["label"])
        title.setProperty("class", "group_title")

        desc = QtWidgets.QLabel(item["description"])
        desc.setProperty("class", "group_description")
        desc.setWordWrap(True)

        text_layout.addWidget(title)
        text_layout.addWidget(desc)

        layout.addWidget(img)
        layout.addLayout(text_layout)

        card.mousePressEvent = lambda e, i=item: self._select_card(i["id"])
        return card

    def _select_card(self, image_id: str) -> None:
        for cid, card in self.image_cards.items():
            card.setProperty("selected", cid == image_id)
            card.style().unpolish(card)
            card.style().polish(card)

        self.selected_image_type = image_id
        self._update_when_to_use()

    def _update_when_to_use(self) -> None:
        if not self.selected_image_type:
            self.widget.when_to_use_content.setText("Selecciona un tipo de imagen")
            return

        item = next(i for i in IMAGE_TYPES if i["id"] == self.selected_image_type)
        self.widget.when_to_use_content.setText(item["when_to_use"])

    # -------------------------
    # Accordion
    # -------------------------
    def _setup_accordion(self) -> None:
        self.widget.extra_content.setVisible(False)
        self.widget.extra_toggle.toggled.connect(self._toggle_extra)

    def _toggle_extra(self, checked: bool) -> None:
        self.widget.extra_content.setVisible(checked)
        self.widget.extra_toggle.setArrowType(
            QtCore.Qt.DownArrow if checked else QtCore.Qt.RightArrow
        )

    # -------------------------
    # Extras
    # -------------------------
    def _load_extras(self) -> None:
        for g in IMAGE_GALLERIES:
            self.widget.gallery_combo.addItem(g["label"], g["id"])
        for c in IMAGE_COMPOSITIONS:
            self.widget.compositon_combo.addItem(c["label"], c["id"])

    def _update_cloud_label(self, value: int) -> None:
        self.widget.cloud_value_label.setText(f"{value}%")
