import math

from qgis.PyQt import QtWidgets, QtCore, QtGui
from frontend.presentation.resources.styles.tokens.theme_light import THEME
from frontend.presentation.resources.styles.tokens.types import Token


class OrbitLoader(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.angle: int = 0
        self.orbit_color = QtGui.QColor(THEME[Token.COLOR_SEPARATOR_LINE])
        self.planet_color = QtGui.QColor(THEME[Token.COLOR_GREEN_LIGHT_300])

        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAutoFillBackground(False)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(30)

    def rotate(self) -> None:
        self.angle = (self.angle + 5) % 360
        self.update()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        rect = self.rect()
        center = rect.center()

        size = min(rect.width(), rect.height())
        radius = max(28, (size // 2) - 18)

        # orbit
        painter.setPen(QtGui.QPen(self.orbit_color, 2))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawEllipse(center, radius, radius)

        # planet orbiting
        angle_rad = math.radians(self.angle)
        x = center.x() + radius * math.cos(angle_rad)
        y = center.y() + radius * math.sin(angle_rad)

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.planet_color)
        painter.drawEllipse(QtCore.QPointF(x, y), 5, 5)
