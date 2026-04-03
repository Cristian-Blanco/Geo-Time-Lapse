from pathlib import Path
from backend.domain.types.time_window import TimeWindow
from backend.domain.config.image_type import IMAGE_TYPES
from collections.abc import Callable

from .composition.composed_image_builder import ComposedImageBuilder
import requests # type: ignore
import ee

class FrameExporter:

    @staticmethod
    def export(
        collection: ee.ImageCollection,
        windows: list[TimeWindow],
        region: ee.Geometry,
        composition: str,
        output_dir: Path,
        gallery_id: str,
        image_type: str,
        dimensions: int = 1920,
        progress_callback: Callable[[int, str], None] | None = None
    ) -> list[Path]:
        image_type_config = IMAGE_TYPES[gallery_id][image_type]
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        exported_files: list[Path] = []

        total = len(windows)

        for index, window in enumerate(windows):
            percent = int((index + 1) / total * 30) + 50  # 50% to 80%

            if progress_callback is not None:
                progress_callback(percent, f"Downloading frame {index+1}/{total}")

            image = ComposedImageBuilder.build(
                composition_id=composition,
                collection=collection,
                start=window["start"],
                end=window["end"],
                region=region,
            )

            vis = {
                "bands": image_type_config["bands"],
                "min": image_type_config["vis_min"],
                "max": image_type_config["vis_max"],
                "dimensions": dimensions,
                "region": region,
                "format": "jpg",
            }

            url = image.getThumbURL(vis)
            response = requests.get(url, timeout=60)
            response.raise_for_status()

            filename = output_path / f'frame_{index:03d}_{window["label"]}.jpg'

            with open(filename, "wb") as file:
                file.write(response.content)

            exported_files.append(filename)

        return exported_files
