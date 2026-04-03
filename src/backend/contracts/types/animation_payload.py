from typing import TypedDict, NotRequired
from collections.abc import Callable

class AnimationPayload(TypedDict):
    project_id: str
    output_dir: str
    template: str

    gallery_id: str
    image_type: str
    composition: str
    cloud_percentage: int | None

    coordinates: list[float]

    temporal_interval_months: int
    start_date: str
    end_date: str
    frame_duration_seconds: int

    progress_callback: Callable[[int, str], None]
    is_cancelled: NotRequired[Callable[[], bool]]
