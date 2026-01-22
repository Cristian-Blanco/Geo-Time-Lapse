from typing import Literal

MODE = Literal["basic", "advanced"]

WIZARD_BLUEPRINT = {
    "start": "login",
    "total_steps": 7,
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
            "next": {"type": "to", "target": "basic_image_type"},
            "step": 3,
        },
        "basic_image_type": {
            "ui": "wizard_basic_02_image_type.ui",
            "controller": "frontend.controllers.pages.basic_image_type:BasicImageType",
            "next": {"type": "to", "target": "basic_time_lapse"},
            "step": 4,
        },
        "basic_time_lapse": {
            "ui": "wizard_basic_03_time_lapse.ui",
            "controller": "frontend.controllers.pages.basic_time_lapse:BasicTimeLapse",
            "next": {"type": "to", "target": "basic_filter"},
            "step": 5,
        },
        "basic_filter": {
            "ui": "wizard_basic_02_filter.ui",
            "controller": "frontend.controllers.pages.basic_filter:BasicFilter",
            "next": {"type": "to", "target": "merge"},
            "step": 6,
        },
        "advanced_intro": {
            "ui": "wizard_03_advanced.ui",
            "controller": "frontend.controllers.pages.advanced_intro_page:AdvancedIntroPage",
            "next": {"type": "to", "target": "merge"},
            "step": 5,
        },
        "merge": {
            "ui": "wizard_04_merge.ui",
            "controller": "frontend.controllers.pages.merge_page:MergePage",
            "next": {"type": "end"},
            "step": 7,
        },
    },
}

ENABLE_ADVANCED_MODE = False
