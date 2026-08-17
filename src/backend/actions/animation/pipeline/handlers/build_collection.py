from backend.contracts.types.animation_payload import AnimationPayload
from backend.actions.animation.pipeline.context import TimeLapseContext
from collections.abc import Callable

from backend.core.pipeline import PipelineHandler

from backend.modules.animation.collection import CollectionRegistry, Gallery

from backend.shared.cancellation import raise_process_cancelled
import ee

class BuildCollectionHandler(PipelineHandler[TimeLapseContext]):

    def handle(self, context: TimeLapseContext) -> TimeLapseContext:

        payload: AnimationPayload = context["payload"]
        region: ee.Geometry = context["region"]
        start_date: str = payload["start_date"]
        end_date: str = payload["end_date"]
        cloud_percentage: int = payload["cloud_percentage"]

        progress: Callable[[int, str], None] = payload["progress_callback"]
        is_cancelled: Callable[[], bool] = payload["is_cancelled"]

        progress(20, "Requesting Google imagery")

        gallery: Gallery = CollectionRegistry.get(
            payload["gallery_id"]
        )

        collection: ee.ImageCollection = gallery.build_collection(
            start_date=start_date,
            end_date=end_date,
            region=region,
            cloud_percentage=cloud_percentage,
        )

        context["gallery"] = gallery
        context["collection"] = collection

        raise_process_cancelled(is_cancelled)

        return context
