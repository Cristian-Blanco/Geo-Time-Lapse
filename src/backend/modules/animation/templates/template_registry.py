from .frame_template import FrameTemplate
from .implementations.simple_label_template import SimpleLabelTemplate
from .implementations.advanced_map_template import AdvancedMapTemplate

class TemplateRegistry:

    _templates: dict[str, type[FrameTemplate]] = {
        "simple": SimpleLabelTemplate,
        "advanced":AdvancedMapTemplate,
    }

    @classmethod
    def get(cls, template_id: str) -> type[FrameTemplate]:
        try:
            return cls._templates[template_id]
        except KeyError as error:
            raise ValueError(f"Template not found: {template_id}") from error
