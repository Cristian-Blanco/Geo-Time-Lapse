from collections.abc import Callable
from qgis.PyQt.QtGui import QColor
from qgis.gui import (
    QgsMapToolEmitPoint,
    QgsRubberBand,
    QgsMapCanvas,
    QgsMapMouseEvent
)
from qgis.core import (
    QgsCoordinateTransform,
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsPointXY,
    QgsRectangle,
    QgsWkbTypes
)

class RectangleMapTool(QgsMapToolEmitPoint):

    def __init__(self, canvas: QgsMapCanvas, on_finish_callback: Callable[[QgsPointXY, QgsPointXY], None]) -> None:
        super().__init__(canvas)
        self.on_finish_callback = on_finish_callback

        self.start_point: QgsPointXY | None = None
        self.end_point: QgsPointXY | None = None

        self.rubber_band = QgsRubberBand(canvas, QgsWkbTypes.PolygonGeometry)
        self.rubber_band.setColor(QColor(255, 0, 0, 100))
        self.rubber_band.setWidth(2)

    def canvasPressEvent(self, event: QgsMapMouseEvent) -> None:
        self.start_point = event.mapPoint()
        self.end_point = self.start_point
        self._update_rubber_band()

    def canvasMoveEvent(self, event: QgsMapMouseEvent) -> None:
        if self.start_point is None:
            return

        self.end_point = event.mapPoint()
        self._update_rubber_band()

    def canvasReleaseEvent(self, event: QgsMapMouseEvent) -> None:
        if self.start_point is None:
            return

        self.end_point = event.mapPoint()

        rect = QgsRectangle(self.start_point, self.end_point)

        source_crs = self.canvas().mapSettings().destinationCrs()

        target_crs = QgsCoordinateReferenceSystem("EPSG:4326")

        transform = QgsCoordinateTransform(
            source_crs,
            target_crs,
            QgsProject.instance()
        )

        # Transform corners
        top_left = transform.transform(rect.xMinimum(), rect.yMaximum())
        bottom_right = transform.transform(rect.xMaximum(), rect.yMinimum())

        # clean selection
        self.rubber_band.reset(QgsWkbTypes.PolygonGeometry)

        # send result in 4326
        self.on_finish_callback(top_left, bottom_right)

        self.start_point = None
        self.end_point = None

    def _update_rubber_band(self) -> None:
        if self.start_point is None or self.end_point is None:
            return

        self.rubber_band.reset(QgsWkbTypes.PolygonGeometry)

        rect = QgsRectangle(self.start_point, self.end_point)

        xmin = rect.xMinimum()
        xmax = rect.xMaximum()
        ymin = rect.yMinimum()
        ymax = rect.yMaximum()

        p1 = QgsPointXY(xmin, ymax)  # top-left
        p2 = QgsPointXY(xmax, ymax)  # top-right
        p3 = QgsPointXY(xmax, ymin)  # bottom-right
        p4 = QgsPointXY(xmin, ymin)  # bottom-left

        self.rubber_band.addPoint(p1, False)
        self.rubber_band.addPoint(p2, False)
        self.rubber_band.addPoint(p3, False)
        self.rubber_band.addPoint(p4, True)
