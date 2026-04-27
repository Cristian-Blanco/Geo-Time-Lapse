from frontend.domain.wizard.types import WizardBlueprint

WIZARD_BLUEPRINT: WizardBlueprint = {
    "start": "login",
    "total_steps": 8,
    "nodes": {
        "login": {
            "ui": "wizard_login.ui",
            "view": "frontend.presentation.views.pages.login_page:LoginPage",
            "next": {"type": "to", "target": "mode"},
            "step": 1,
        },
        "mode": {
            "ui": "wizard_mode.ui",
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
            "ui": "wizard_basic_image_type.ui",
            "view": "frontend.presentation.views.pages.basic_image_type:BasicImageType",
            "next": {"type": "to", "target": "basic_points_map"},
            "step": 3,
        },
        "basic_points_map": {
            "ui": "wizard_basic_points_map.ui",
            "view": "frontend.presentation.views.pages.basic_points_map:BasicPointsMap",
            "next": {"type": "to", "target": "basic_time_lapse"},
            "step": 4,
        },
        "basic_time_lapse": {
            "ui": "wizard_basic_time_lapse.ui",
            "view": "frontend.presentation.views.pages.basic_time_lapse:BasicTimeLapse",
            "next": {"type": "to", "target": "template_selection"},
            "step": 5,
        },
        "template_selection": {
            "ui": "wizard_template_selection.ui",
            "view": "frontend.presentation.views.pages.template_selection:TemplateSelection",
            "next": {"type": "to", "target": "directory_selection"},
            "step": 6,
        },
        "directory_selection": {
            "ui": "wizard_directory_selection.ui",
            "view": "frontend.presentation.views.pages.directory_selection:DirectorySelection",
            "next": {"type": "to", "target": "processing"},
            "step": 7,
        },
        "advanced_intro": {
            "ui": "wizard_advanced.ui",
            "view": "frontend.presentation.views.pages.advanced_intro_page:AdvancedIntroPage",
            "next": {"type": "to", "target": "template_selection"},
            "step": 5,
        },
        "processing": {
            "ui": "wizard_loading.ui",
            "view": "frontend.presentation.views.pages.processing_progress:ProcessingProgress",
            "next": {"type": "end"},
            "step": 8
        }
    },
}
