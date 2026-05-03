from frontend.presentation.views.base_page import BasePage
from frontend.store.wizard_context import WizardContext
from frontend.domain.imagery import Catalog, TEMPORAL_CONFIGURATIONS
from qgis.PyQt import QtWidgets, QtCore
from qgis.core import QgsSettings
from qgis.PyQt.QtGui import QIcon
from frontend.config.paths import ICONS_DIR
from math import floor

class BasicTimeLapse(BasePage):
    left_mode = "previous"
    right_mode = "next"

    # -------------------- lifecycle -----------------------

    def __init__(self, widget: QtWidgets.QWidget, state: WizardContext) -> None:
        super().__init__(widget, state)

        self.title = self.tr("Time period")
        self.description = self.tr("Select the range for the timelapse")

        lang = QgsSettings().value("locale/userLocale")
        self.locale = QtCore.QLocale(lang) if lang else QtCore.QLocale()

        # find childs
        self.date_start = self.widget.findChild(QtWidgets.QDateEdit, "date_start")
        self.date_end = self.widget.findChild(QtWidgets.QDateEdit, "date_end")
        self.lbl_available_date = self.widget.findChild(QtWidgets.QLabel, "lbl_available_date")

        self.cmb_temporal_configuration = self.widget.findChild(QtWidgets.QComboBox, "cmb_temporal_configuration")
        self.spn_frame_duration = self.widget.findChild(QtWidgets.QSpinBox, "spn_frame_duration")
        self.lbl_generated_images = self.widget.findChild(QtWidgets.QLabel, "lbl_generated_images")
        self.lbl_video_duration = self.widget.findChild(QtWidgets.QLabel, "lbl_video_duration")
        self.lbl_image_type = self.widget.findChild(QtWidgets.QLabel, "lbl_image_type")
        self.lbl_satellite = self.widget.findChild(QtWidgets.QLabel, "lbl_satellite")
        self.lbl_cloud_percentage = self.widget.findChild(QtWidgets.QLabel, "lbl_cloud_percentage")
        self.fr_cloud_cover = self.widget.findChild(QtWidgets.QFrame, "fr_cloud_cover")

        # Setup
        self._apply_child_assets()
        self._setup_temporal_configuration()
        self._setup_frame_duration()
        self._setup_date_inputs()

    def on_enter(self) -> None:
        self._set_summary()
        self._set_default_dates()
        self._update_generated_images()
        super().on_enter()

    # --------------------- setup ----------------------------

    def _set_default_dates(self) -> None:
        if not self.date_start or not self.date_end:
            return

        today = QtCore.QDate.currentDate()
        gallery_start_date = Catalog.get_gallery_start_date(self.state.gallery_id)
        if not gallery_start_date:
            return

        default_start_date = QtCore.QDate.fromString(gallery_start_date, "yyyy-MM-dd")
        if not default_start_date.isValid():
            return

        self.date_start.blockSignals(True)
        self.date_end.blockSignals(True)

        self.date_start.setMinimumDate(default_start_date)
        self.date_start.setMaximumDate(today)

        self.date_end.setMinimumDate(default_start_date)
        self.date_end.setMaximumDate(today)

        state_start_date = QtCore.QDate.fromString(self.state.start_date or "", "yyyy-MM-dd")
        state_end_date = QtCore.QDate.fromString(self.state.end_date or "", "yyyy-MM-dd")

        if state_start_date.isValid():
            self.date_start.setDate(state_start_date)
        else:
            self.date_start.setDate(default_start_date)

        if state_end_date.isValid():
            self.date_end.setDate(state_end_date)
        else:
            self.date_end.setDate(today)

        self.date_start.blockSignals(False)
        self.date_end.blockSignals(False)

        # Set date message available for the first image.
        formatted = self.locale.toString(default_start_date, "MMMM yyyy")
        text = self.tr("Available data from: {date}").format(date=formatted)
        self.lbl_available_date.setText(text)

        self._sync_dates_to_state()

    def _setup_temporal_configuration(self) -> None:
        if not self.cmb_temporal_configuration:
            return

        self.cmb_temporal_configuration.clear()

        for item in TEMPORAL_CONFIGURATIONS:
            self.cmb_temporal_configuration.addItem(self.tr(item["label"]), item["months"])

        recommended_item = Catalog.get_recommended_temporal_configuration()
        recommended_index = self.cmb_temporal_configuration.findData(recommended_item["months"])

        if recommended_index >= 0:
            self.cmb_temporal_configuration.setCurrentIndex(recommended_index)
            self.state.temporal_interval_months = recommended_item["months"]

        self.cmb_temporal_configuration.currentIndexChanged.connect(self._on_temporal_configuration_changed)

    def _setup_frame_duration(self) -> None:
        if not self.spn_frame_duration:
            return

        self.state.frame_duration_seconds = self.spn_frame_duration.value()
        self.spn_frame_duration.valueChanged.connect(self._on_frame_duration_changed)

    def _setup_date_inputs(self) -> None:
        if self.date_start:
            self.date_start.dateChanged.connect(self._on_dates_changed)

        if self.date_end:
            self.date_end.dateChanged.connect(self._on_dates_changed)

    def _apply_child_assets(self) -> None:
        icon_map = {
            "icon_filter": "radar.png",
            "icon_satellite": "satellite.png",
            "icon_cloud": "cloud.png",
        }

        for obj_name, icon_file in icon_map.items():
            btn = self.widget.findChild(QtWidgets.QToolButton, obj_name)
            if btn:
                btn.setIcon(QIcon(str(ICONS_DIR / icon_file)))
                btn.setIconSize(QtCore.QSize(24, 24))

    def _set_summary(self) -> None:
        image_type_label = Catalog.get_image_type_label(self.state.image_type)
        gallery_label = Catalog.get_gallery_label(self.state.gallery_id)

        if self.lbl_image_type:
            self.lbl_image_type.setText(image_type_label or "-")

        if self.lbl_satellite:
            self.lbl_satellite.setText(gallery_label or "-")

        is_radar = self.state.image_type == "radar"

        if self.fr_cloud_cover:
            self.fr_cloud_cover.setVisible(not is_radar)

        if self.lbl_cloud_percentage and not is_radar:
            if self.state.cloud_percentage is not None:
                self.lbl_cloud_percentage.setText(f"{self.state.cloud_percentage} %")
            else:
                self.lbl_cloud_percentage.setText("-")

    # -------------------- Event handlers --------------------

    def _on_dates_changed(self) -> None:
        self._sync_dates_to_state()
        self.validityChanged.emit(self.is_valid())
        self._update_generated_images()

    def _on_temporal_configuration_changed(self) -> None:
        if not self.cmb_temporal_configuration:
            return

        months = self.cmb_temporal_configuration.currentData()
        if isinstance(months, int):
            self.state.temporal_interval_months = months

        self.validityChanged.emit(self.is_valid())
        self._update_generated_images()

    def _on_frame_duration_changed(self, value: int) -> None:
        self.state.frame_duration_seconds = value
        self._update_video_duration()

    # ---------------------- Sync state ----------------------

    def _sync_dates_to_state(self) -> None:
        if not self.date_start or not self.date_end:
            return

        self.state.start_date = self.date_start.date().toString("yyyy-MM-dd")
        self.state.end_date = self.date_end.date().toString("yyyy-MM-dd")

    def is_valid(self) -> bool:
        if not self.date_start or not self.date_end:
            return False

        interval_months = self.state.temporal_interval_months
        if interval_months is None:
            return False

        start_date = self.date_start.date()
        end_date = self.date_end.date()

        total_months = self._full_months_between(start_date, end_date)
        return total_months >= interval_months

    # ---------------------- calculations ------------------------

    def _update_generated_images(self) -> None:
        if not self.lbl_generated_images:
            return

        image_count = self._calculate_generated_images()
        self.state.generated_images = image_count

        status_icon = "🟢" if image_count > 0 else "🔴"

        text = self.tr(
            "{icon} This configuration will generate at least: {count} images"
        ).format(
            icon=status_icon,
            count=image_count
        )

        self.lbl_generated_images.setText(text)

        self._update_video_duration()

    def _calculate_generated_images(self) -> int:
        if not self.date_start or not self.date_end:
            return 0

        interval_months = self.state.temporal_interval_months
        if interval_months is None:
            return 0

        start_date = self.date_start.date()
        end_date = self.date_end.date()

        total_months = self._full_months_between(start_date, end_date)

        if total_months < interval_months:
            return 0

        return floor(total_months / interval_months)


    def _full_months_between(self, start_date: QtCore.QDate, end_date: QtCore.QDate) -> int:
        months: int = (end_date.year() - start_date.year()) * 12 + (end_date.month() - start_date.month())

        if end_date.day() < start_date.day():
            months -= 1

        if months < 0:
            return 0

        return months

    def _update_video_duration(self) -> None:
        if not self.lbl_video_duration or not self.spn_frame_duration:
            return

        frame_duration = self.spn_frame_duration.value()
        image_count = self.state.generated_images or 0

        total_seconds = image_count * frame_duration

        self.state.frame_duration_seconds = frame_duration

        self.lbl_video_duration.setText(
            self.tr("This configuration will last for: {seconds} seconds").format(
                seconds=total_seconds
            )
        )
