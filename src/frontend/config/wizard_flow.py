from typing import Literal

MODE = Literal["basic", "advanced"]

WIZARD_BLUEPRINT = {
    "start": "login",
    "total_steps": 4,
    "nodes": {
        "login": {
            "ui": "wizard_01_login.ui",
            "controller": "frontend.controllers.pages.login_page:LoginPage",
            "next": {"type": "to", "target": "mode"},
            "step": 1,
        },
        "mode": {
            "ui": "wizard_02_mode.ui",
            "controller": "frontend.controllers.pages.mode_page:ModePage",
            "next": {
                "type": "switch",
                "cases": {"basic": "basic_intro", "advanced": "advanced_intro"},
                "default": "basic_intro",
                "switch_on": "mode",
            },
            "step": 2,
        },
        "basic_intro": {
            "ui": "wizard_03_basic.ui",
            "controller": "frontend.controllers.pages.basic_intro_page:BasicIntroPage",
            "next": {"type": "to", "target": "merge"},
            "step": 3,
        },
        "advanced_intro": {
            "ui": "wizard_03_advanced.ui",
            "controller": "frontend.controllers.pages.advanced_intro_page:AdvancedIntroPage",
            "next": {"type": "to", "target": "merge"},
            "step": 3,
        },
        "merge": {
            "ui": "wizard_04_merge.ui",
            "controller": "frontend.controllers.pages.merge_page:MergePage",
            "next": {"type": "end"},
            "step": 4,
        },
    },
}

ENABLE_ADVANCED_MODE = False
