from backend.contracts.types.animation_payload import AnimationPayload
from backend.actions.animation.pipeline.context import TimeLapseContext
from collections.abc import Callable

from backend.modules.google_earth_engine import EEInitializer
from backend.core.pipeline import PipelineHandler

class InitializeEEHandler(PipelineHandler[TimeLapseContext]):

    def handle(self, context: TimeLapseContext) -> TimeLapseContext:

        payload: AnimationPayload = context["payload"]
        progress: Callable[[int, str], None] = payload["progress_callback"]

        progress(10, "Preparing export")

        EEInitializer.initialize(project_id=payload["project_id"])

        return context
