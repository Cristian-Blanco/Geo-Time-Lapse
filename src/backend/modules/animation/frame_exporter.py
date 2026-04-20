from pathlib import Path
from backend.domain.types.time_window import TimeWindow
from backend.domain.types.image_type_config import ImageTypeDefinition
from backend.shared.cancellation import raise_process_cancelled
from collections.abc import Callable

from .composition import CompositionRegistry

import requests # type: ignore[import, unused-ignore]
import ee

class FrameExporter:

    def __init__(
        self,
        composition_id: str,
        vis_params: ImageTypeDefinition,
        output_dir: Path,
        dimensions: int = 1920,
    ) -> None:
        self.composition = CompositionRegistry.get(composition_id)
        self.output_dir = output_dir
        self.vis_params = vis_params
        self.dimensions = dimensions


    def export(
        self,
        collection: ee.ImageCollection,
        windows: list[TimeWindow],
        region: ee.Geometry,
        progress_callback: Callable[[int, str], None] | None = None,
        is_cancelled: Callable[[], bool] | None = None
    ) -> list[Path]:

        self.output_dir.mkdir(parents=True, exist_ok=True)

        exported_files: list[Path] = []

        total = len(windows)

        for index, window in enumerate(windows):
            raise_process_cancelled(is_cancelled)

            percent = int((index + 1) / total * 30) + 50  # 50% to 80%

            if progress_callback is not None:
                progress_callback(percent, "Downloading frames...")

            filtered_collection = collection.filterDate(window["start"], window["end"])
            image = self.composition.build(filtered_collection, region)

            vis = {
                "bands": self.vis_params["bands"],
                "min": self.vis_params["vis_min"],
                "max": self.vis_params["vis_max"],
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
