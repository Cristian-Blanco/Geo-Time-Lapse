from typing import TypedDict, NotRequired
from pathlib import Path

from backend.contracts.types.animation_payload import AnimationPayload
from backend.domain.types.time_window import TimeWindow
from backend.modules.animation.collection import Gallery

import ee

class TimeLapseContext(TypedDict):
    payload: AnimationPayload

    region: NotRequired[ee.Geometry]
    gallery: NotRequired[Gallery]
    collection: NotRequired[ee.ImageCollection]

    windows: NotRequired[list[TimeWindow]]
    bbox: NotRequired[tuple[float, float, float, float]]

    vis_params: NotRequired[dict]

    frames_dir: NotRequired[Path]
    frame_paths: NotRequired[list[Path | None]]
    templated_frames: NotRequired[list[Path]]

    video_path: NotRequired[Path]
