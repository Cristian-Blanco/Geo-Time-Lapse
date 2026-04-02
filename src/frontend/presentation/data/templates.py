from frontend.config.paths import ICONS_DIR
from frontend.domain.templates.types import TemplateDef

TEMPLATES: TemplateDef = [
    {
        "id": "template_1",
        "title": "Basic Timelapse",
        "description": "Recommended for general timelapse use.",
        "icon": str(ICONS_DIR / "template_1.png"),
        "enabled": True,
    },
    {
        "id": "template_2",
        "title": "Annotated Date Overlay",
        "description": "Caption, title, and descriptions of the displayed date are added.",
        "icon": str(ICONS_DIR / "template_2.png"),
        "enabled": False,
    },
    # {
    #     "id": "template_3",
    #     "title": "Template 3",
    #     "description": "Is simply dummy text of the printing and typesetting industry.",
    #     "icon": str(ICONS_DIR / "template_2.png"),
    #     "enabled": False,
    # },
]
