import ee
from .composition_registry import CompositionRegistry


class ComposedImageBuilder:
    @staticmethod
    def build(
        composition_id: str,
        collection: ee.ImageCollection,
        start: ee.Date,
        end: ee.Date,
        region: ee.Geometry,
    ) -> ee.Image:
        filtered_collection = collection.filterDate(start, end)
        composition = CompositionRegistry.get(composition_id)

        return composition.build(filtered_collection, region)
