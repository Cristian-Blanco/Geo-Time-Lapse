from qgis.core import QgsDistanceArea, QgsGeometry, QgsRectangle

def calculate_area_km2(xmin: float, ymin: float, xmax: float, ymax: float) -> float:
        d = QgsDistanceArea()
        d.setEllipsoid('WGS84')

        rect = QgsRectangle(xmin, ymin, xmax, ymax)
        geom = QgsGeometry.fromRect(rect)

        area_m2 = float(d.measureArea(geom))
        return area_m2 / 1_000_000  # km²
