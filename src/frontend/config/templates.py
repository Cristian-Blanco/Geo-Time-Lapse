from .paths import ICONS_DIR

TEMPLATES = [
    {
        "id": "template_1",
        "title": "Template 1",
        "description": "Recommended for general timelapse use.",
        "icon": str(ICONS_DIR / "template_1.png"),
        "enabled": True,
    },
    {
        "id": "template_2",
        "title": "Template 2",
        "description": "Caption, title, and descriptions of the displayed date are added.",
        "icon": str(ICONS_DIR / "template_2.png"),
        "enabled": False,
    },
    {
        "id": "template_3",
        "title": "Template 3",
        "description": "Is simply dummy text of the printing and typesetting industry.",
        "icon": str(ICONS_DIR / "template_2.png"),
        "enabled": False,
    },
]
