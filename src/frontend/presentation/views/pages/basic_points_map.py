from frontend.presentation.views.base_page import BasePage
from frontend.store.wizard_context import WizardContext
from qgis.PyQt import QtWidgets, QtCore
from qgis.PyQt.QtGui import QIcon
from frontend.config.paths import ICONS_DIR
from qgis.utils import iface
from frontend.presentation.workers.map_tools import RectangleMapTool
from qgis.core import QgsPointXY
from frontend.domain.geo.bbox import get_valid_bbox_from_strings
from frontend.infrastructure.geo.area_calculator import calculate_area_km2

class BasicPointsMap(BasePage):
    left_mode = "previous"
    right_mode = "next"

    def __init__(self, widget: QtWidgets.QWidget, state: WizardContext) -> None:
        super().__init__(widget, state)

        self.title = self.tr("Video area")
        self.description = self.tr("Define the geographic area that will be used to generate the timelapse.")
        self.canvas = iface.mapCanvas()

        self.points_map_status = widget.findChild(QtWidgets.QLabel, "points_map_status")
        self.lbl_area_info = widget.findChild(QtWidgets.QLabel, "lbl_area_info")

        self.lat_p1 = widget.findChild(QtWidgets.QLineEdit, "lat_p1")
        self.lon_p1 = widget.findChild(QtWidgets.QLineEdit, "long_p1")
        self.lat_p2 = widget.findChild(QtWidgets.QLineEdit, "lat_p2")
        self.lon_p2 = widget.findChild(QtWidgets.QLineEdit, "lon_p2")

        self.change_wizard: bool = False

        self._apply_child_assets()
        self._connect_accordion()
        self._connect_manual_inputs()

    def _apply_child_assets(self) -> None:
        pin_png = str(ICONS_DIR / "location.png")
        btn = self.widget.findChild(QtWidgets.QPushButton, "btn_select_map")
        if btn:
            btn.setIcon(QIcon(pin_png))
            btn.setIconSize(QtCore.QSize(18, 18))
            btn.clicked.connect(self._activate_rectangle_tool)

    def _connect_accordion(self) -> None:
        toggle_btn = self.widget.findChild(QtWidgets.QToolButton, "btn_manual_toggle")
        body = self.widget.findChild(QtWidgets.QWidget, "manual_body")

        if not toggle_btn or not body:
            return

        body.setVisible(toggle_btn.isChecked())
        self._update_arrow(toggle_btn)

        toggle_btn.toggled.connect(lambda checked: self._toggle_manual_body(checked, body, toggle_btn))

    def _toggle_manual_body(
        self,
        checked: bool,
        body: QtWidgets.QWidget,
        btn: QtWidgets.QToolButton,
    ) -> None:
        body.setVisible(checked)
        self._update_arrow(btn)

    def _update_arrow(self, btn: QtWidgets.QToolButton) -> None:
        btn.setArrowType(QtCore.Qt.DownArrow if btn.isChecked() else QtCore.Qt.RightArrow)

    def _activate_rectangle_tool(self) -> None:

        self.points_map_status.setText(self.tr("🟠 Waiting for selection on the map"))
        # Guardar herramienta anterior
        self.previous_tool = self.canvas.mapTool()

        # Hide dialog
        self.dialog = self.widget.window()
        self.dialog.lower()
        self.canvas.setFocus()

        self.map_tool = RectangleMapTool(self.canvas, self._on_rectangle_selected)
        self.canvas.setMapTool(self.map_tool)

    def _on_rectangle_selected(self, top_left: QgsPointXY, bottom_right: QgsPointXY) -> None:
        # Open dialog
        if self.dialog:
            self.dialog.raise_()
            self.dialog.activateWindow()

        self.canvas.setMapTool(self.previous_tool)

        xmin = top_left.x()
        ymax = top_left.y()

        xmax = bottom_right.x()
        ymin = bottom_right.y()

        lat_p1 = self.widget.findChild(QtWidgets.QLineEdit, "lat_p1")
        lon_p1 = self.widget.findChild(QtWidgets.QLineEdit, "long_p1")
        lat_p2 = self.widget.findChild(QtWidgets.QLineEdit, "lat_p2")
        lon_p2 = self.widget.findChild(QtWidgets.QLineEdit, "lon_p2")

        if lat_p1 and lon_p1:
            lat_p1.setText(str(ymax))
            lon_p1.setText(str(xmin))

        if lat_p2 and lon_p2:
            lat_p2.setText(str(ymin))
            lon_p2.setText(str(xmax))

        self.change_wizard = True
        self.validityChanged.emit(self.is_valid())

        area_km2 = calculate_area_km2(xmin, ymin, xmax, ymax)

        max_area = self.state.max_area_km2 or 200  # fallback

        # mensaje base
        text_area = f"Area: {area_km2:.2f} km²"
        text_selected = "🟢 Selected coordinates"

        # alerta dinámica
        if max_area is not None and area_km2 > max_area:
            text_area += f" (Large area detected. Recommended ≤ {max_area} km²)"
            text_selected = "🟡 Selected coordinates"

        # actualizar UI
        if self.lbl_area_info:
            self.points_map_status.setText(self.tr(text_selected))
            self.lbl_area_info.setText(self.tr(text_area))

    def _connect_manual_inputs(self) -> None:
        for field in [self.lat_p1, self.lon_p1, self.lat_p2, self.lon_p2]:
            if field:
                field.textChanged.connect(self._on_manual_coordinates_changed)

    def _on_manual_coordinates_changed(self) -> None:
        bbox = get_valid_bbox_from_strings(
            self.lat_p1.text(),
            self.lon_p1.text(),
            self.lat_p2.text(),
            self.lon_p2.text(),
        )

        if bbox is None:
            self.points_map_status.setText(self.tr("🔴 Please enter valid WGS84 coordinates"))
            if self.lbl_area_info:
                self.lbl_area_info.setText("")

            self.change_wizard = False
            self.validityChanged.emit(self.is_valid())
            return

        xmin, ymin, xmax, ymax = bbox
        area_km2 = calculate_area_km2(xmin, ymin, xmax, ymax)
        max_area = self.state.max_area_km2 or 200

        self.state.coordinates = [xmin, ymin, xmax, ymax]

        text_selected = "🟢 Selected coordinates"
        text_area = f"Area: {area_km2:.2f} km²"

        if max_area is not None and area_km2 > max_area:
            text_selected = "🟡 Selected coordinates"
            text_area += f" (Large area detected. Recommended ≤ {max_area} km²)"

        self.points_map_status.setText(self.tr(text_selected))
        if self.lbl_area_info:
            self.lbl_area_info.setText(self.tr(text_area))

        self.change_wizard = True
        self.validityChanged.emit(self.is_valid())

    def is_valid(self) -> bool:
        return self.change_wizard and self.state.coordinates is not None
