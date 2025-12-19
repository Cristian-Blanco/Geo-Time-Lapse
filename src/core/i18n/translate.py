from qgis.PyQt.QtCore import QCoreApplication

CONTEXT = "GeoTimeLapse"

def translate(text: str) -> str:
    return QCoreApplication.translate(CONTEXT, text)
