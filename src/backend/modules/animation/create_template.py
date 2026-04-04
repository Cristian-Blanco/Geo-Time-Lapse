from pathlib import Path
from PIL import Image

from backend.domain.types.time_window import TimeWindow
from .templates.template_registry import TemplateRegistry

class CreateTemplate:

    @staticmethod
    def apply(
        frames: list[Path],
        windows: list[TimeWindow],
        template_id: str,
        output_dir: Path,
    ) -> list[Path]:

        template_cls = TemplateRegistry.get(template_id)

        output_dir.mkdir(parents=True, exist_ok=True)

        result: list[Path] = []

        for frame_path, window in zip(frames, windows):

            try:
                with Image.open(frame_path) as image:
                    image_rgb = image.convert("RGB")

                    templated = template_cls.apply(image_rgb, window)

                    output_path = output_dir / frame_path.name
                    templated.save(output_path)

                    result.append(output_path)

            except Exception as error:
                raise RuntimeError(f"Error applying template '{template_id}': {str(error)}") from error

        return result
