from dataclasses import dataclass
from frontend.domain.wizard.types import Mode, WizardState

@dataclass
class WizardContext(WizardState):
    project_id: str = ""
    authenticated: bool = False
    mode: Mode | None = None
    template: str | None = None
    output_dir: str | None = None
    verified: bool = False

    # ----- Image Selection ----
    image_type: str | None = None
    gallery_id: str | None = None
    composition: str | None = None
    cloud_percentage: int | None = None
    check_normalize_images: bool = True
    max_area_km2: int | None = None

    # ------ Coordinates -------
    coordinates: list[float] | None = None

    # -- Temporal configuration --
    temporal_interval_months: int | None = None
    start_date: str | None = None
    end_date: str | None = None
    frame_duration_seconds: int | None = None
    generated_images: int | None = None
