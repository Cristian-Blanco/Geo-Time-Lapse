from typing import Literal

MODE = Literal["basic", "advanced"]

WIZARD_BLUEPRINT = {
    "start": "login",
    "total_steps": 5,
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
                "cases": {"basic": "basic_points_map", "advanced": "advanced_intro"},
                "default": "basic_points_map",
                "switch_on": "mode",
            },
            "step": 2,
        },
        "basic_points_map": {
            "ui": "wizard_basic_01_points_map.ui",
            "controller": "frontend.controllers.pages.basic_points_map:BasicPointsMap",
            "next": {"type": "to", "target": "basic_filter"},
            "step": 3,
        },
        "basic_filter": {
            "ui": "wizard_basic_02_filter.ui",
            "controller": "frontend.controllers.pages.basic_filter:BasicFilter",
            "next": {"type": "to", "target": "merge"},
            "step": 4,
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
            "step": 5,
        },
    },
}

ENABLE_ADVANCED_MODE = True
