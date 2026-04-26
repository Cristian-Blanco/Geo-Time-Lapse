from pathlib import Path
from PIL import Image

from backend.domain.types.time_window import TimeWindow
from .templates.template_registry import TemplateRegistry

class CreateTemplate:

    @staticmethod
    def apply(
        frames: list[Path | None],
        windows: list[TimeWindow],
        template_id: str,
        output_dir: Path,
    ) -> list[Path]:

        template_cls = TemplateRegistry.get(template_id)

        output_dir.mkdir(parents=True, exist_ok=True)

        # Set image dimensions based on a successfully downloaded image
        first_valid_frame = next((frame for frame in frames if frame is not None), None)
        if first_valid_frame is not None:
            with Image.open(first_valid_frame) as image:
                target_size = image.size
        else:
            target_size = (1920, 1080)

        result: list[Path] = []

        for index, (frame_path, window) in enumerate(zip(frames, windows)):

            try:
                if frame_path is None: # We apply a template with the message "Image not found"
                    templated = template_cls.apply_missing(window=window, size=target_size)

                else:
                    with Image.open(frame_path) as image:
                        image_rgb = image.convert("RGB")
                        image_rgb = image_rgb.resize(target_size)
                        templated = template_cls.apply(image_rgb, window)

                output_path = output_dir / f'frame_{index:03d}_{window["label"]}.jpg'
                templated.save(output_path)

                result.append(output_path)

            except Exception as error:
                raise RuntimeError(f"Error applying template '{template_id}': {str(error)}") from error

        return result
