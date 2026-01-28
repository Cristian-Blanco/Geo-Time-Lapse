from qgis.PyQt import QtWidgets

from frontend.helpers.load_qss import load_qss
from frontend.config.paths import STYLES_DIR
from frontend.resources.styles.tokens.theme_light import THEME


class StyleBootstrap:
    _cached_qss: str | None = None

    @classmethod
    def apply(cls, root: QtWidgets.QWidget) -> None:
        # if cls._cached_qss is None:
        # cls._cached_qss = load_qss(
        #     STYLES_DIR / "base.qss",
        #     STYLES_DIR / "components.qss",
        # )

        # root.setStyleSheet(cls._cached_qss)

        # root.style().unpolish(root)
        # root.style().polish(root)

        qss = load_qss(
            STYLES_DIR / "base" / "base.qss",
            STYLES_DIR / "base" / "typography.qss",

            # Components
            STYLES_DIR / "components" / "progress.qss",
            STYLES_DIR / "components" / "buttons.qss",
            STYLES_DIR / "components" / "date.qss",
            STYLES_DIR / "components" / "inputs.qss",
            STYLES_DIR / "components" / "cards.qss",
            STYLES_DIR / "components" / "scroll.qss",

            # Sections
            STYLES_DIR / "sections" / "header.qss",
            STYLES_DIR / "sections" / "footer.qss",

            # Pages
            STYLES_DIR / "pages" / "login.qss",
            STYLES_DIR / "pages" / "basic_image_type.qss",
            STYLES_DIR  / "pages" / "basic_time_lapse.qss",

            variables={k.value: v for k, v in THEME.items()},
        )

        # Clean and reload styles
        root.setStyleSheet("")
        root.style().unpolish(root)
        root.style().polish(root)

        root.setStyleSheet(qss)

        for w in root.findChildren(QtWidgets.QWidget):
            w.style().unpolish(w)
            w.style().polish(w)
            w.update()

        root.update()
