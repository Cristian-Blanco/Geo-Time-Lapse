from frontend.domain.wizard.types import WizardBlueprint

WIZARD_BLUEPRINT: WizardBlueprint = {
    "start": "login",
    "total_steps": 8,
    "nodes": {
        "login": {
            "ui": "wizard_01_login.ui",
            "view": "frontend.presentation.views.pages.login_page:LoginPage",
            "next": {"type": "to", "target": "mode"},
            "step": 1,
        },
        "mode": {
            "ui": "wizard_02_mode.ui",
            "view": "frontend.presentation.views.pages.mode_page:ModePage",
            "next": {
                "type": "switch",
                "cases": {"basic": "basic_image_type", "advanced": "advanced_intro"},
                "default": "basic_points_map",
                "switch_on": "mode",
            },
            "step": 2,
        },
        "basic_image_type": {
            "ui": "wizard_basic_02_image_type.ui",
            "view": "frontend.presentation.views.pages.basic_image_type:BasicImageType",
            "next": {"type": "to", "target": "basic_points_map"},
            "step": 3,
        },
        "basic_points_map": {
            "ui": "wizard_basic_01_points_map.ui",
            "view": "frontend.presentation.views.pages.basic_points_map:BasicPointsMap",
            "next": {"type": "to", "target": "basic_time_lapse"},
            "step": 4,
        },
        "basic_time_lapse": {
            "ui": "wizard_basic_03_time_lapse.ui",
            "view": "frontend.presentation.views.pages.basic_time_lapse:BasicTimeLapse",
            "next": {"type": "to", "target": "choose_template"},
            "step": 5,
        },
        "choose_template": {
            "ui": "wizard_04_choose_template.ui",
            "view": "frontend.presentation.views.pages.choose_template:ChooseTemplate",
            "next": {"type": "to", "target": "choose_directory"},
            "step": 6,
        },
        "choose_directory": {
            "ui": "wizard_05_choose_directory.ui",
            "view": "frontend.presentation.views.pages.choose_directory:ChooseDirectory",
            "next": {"type": "to", "target": "merge"},
            "step": 7,
        },
        "advanced_intro": {
            "ui": "wizard_03_advanced.ui",
            "view": "frontend.presentation.views.pages.advanced_intro_page:AdvancedIntroPage",
            "next": {"type": "to", "target": "choose_template"},
            "step": 4,
        },
        "merge": {
            "ui": "wizard_04_merge.ui",
            "view": "frontend.presentation.views.pages.merge_page:MergePage",
            "next": {"type": "end"},
            "step": 8,
        },
    },
}
