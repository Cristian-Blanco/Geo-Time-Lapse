from pathlib import Path
from backend.domain.types.time_window import TimeWindow
from collections.abc import Callable

from backend.domain.config.image_type import IMAGE_TYPES
from .composition import CompositionRegistry

import requests # type: ignore
import ee

class FrameExporter:

    def __init__(
        self,
        composition_id: str,
        gallery_id: str,
        image_type: str,
        output_dir: Path,
        dimensions: int = 1920,
    ) -> None:
        self.image_type_config = IMAGE_TYPES[gallery_id][image_type]
        self.composition = CompositionRegistry.get(composition_id)
        self.output_dir = output_dir

        self.dimensions = dimensions


    def export(
        self,
        collection: ee.ImageCollection,
        windows: list[TimeWindow],
        region: ee.Geometry,
        progress_callback: Callable[[int, str], None] | None = None
    ) -> list[Path]:

        self.output_dir.mkdir(parents=True, exist_ok=True)

        exported_files: list[Path] = []

        total = len(windows)

        for index, window in enumerate(windows):
            percent = int((index + 1) / total * 30) + 50  # 50% to 80%

            if progress_callback is not None:
                progress_callback(percent, "Downloading frames...")

            filtered_collection = collection.filterDate(window["start"], window["end"])
            image = self.composition.build(filtered_collection, region)

            vis = {
                "bands": self.image_type_config["bands"],
                "min": self.image_type_config["vis_min"],
                "max": self.image_type_config["vis_max"],
                "dimensions": self.dimensions,
                "region": region,
                "format": "jpg",
            }

            url = image.getThumbURL(vis)
            response = requests.get(url, timeout=60)
            response.raise_for_status()

            filename = self.output_dir / f'frame_{index:03d}_{window["label"]}.jpg'

            with open(filename, "wb") as file:
                file.write(response.content)

            exported_files.append(filename)

        return exported_files
