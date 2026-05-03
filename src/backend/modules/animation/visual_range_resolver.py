from backend.domain.config.image_type import IMAGE_TYPES
from backend.domain.types.image_type_config import ImageTypeDefinition
import ee

class VisualRangeResolver:

    @staticmethod
    def resolve(
        collection: ee.ImageCollection,
        region: ee.Geometry,
        gallery_id: str,
        image_type: str,
        normalize_images: bool,
        is_optical: bool,
    ) -> ImageTypeDefinition:

        config = IMAGE_TYPES[gallery_id][image_type]

        bands = config["bands"]

        if not is_optical or not normalize_images:
            return {
                "bands": bands,
                "vis_min": config["vis_min"],
                "vis_max": config["vis_max"],
            }

        reference_img = collection.median().clip(region)

        stats = reference_img.select(bands).reduceRegion(
            reducer=ee.Reducer.percentile([2, 98]),
            geometry=region,
            scale=config["scale"],
            bestEffort=True,
            maxPixels=1e9,
        ).getInfo()

        mins = [stats[f"{band}_p2"] for band in bands]
        maxs = [stats[f"{band}_p98"] for band in bands]

        return {
            "bands": bands,
            "vis_min": mins,
            "vis_max": maxs,
        }
