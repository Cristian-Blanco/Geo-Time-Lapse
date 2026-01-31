from frontend.config.paths import STYLES_DIR

WIZARD_QSS = [
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
]
