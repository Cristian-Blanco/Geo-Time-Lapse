from backend.contracts.types.animation_payload import AnimationPayload
from backend.actions.animation.pipeline.context import TimeLapseContext

from backend.core.pipeline import PipelineHandler

import ee

class BuildRegionHandler(PipelineHandler[TimeLapseContext]):

    def handle(self, context: TimeLapseContext) -> TimeLapseContext:

        payload: AnimationPayload = context["payload"]

        # [min_lon, min_lat, max_lon, max_lat]
        coordinates: list[float] = payload["coordinates"]

        context["region"] = ee.Geometry.Rectangle(coordinates)

        return context
