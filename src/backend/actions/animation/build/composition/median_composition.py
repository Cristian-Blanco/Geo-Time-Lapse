import ee
from .image_composition import ImageComposition


class MedianComposition(ImageComposition):
    @staticmethod
    def build(
        collection: ee.ImageCollection,
        region: ee.Geometry,
    ) -> ee.Image:
        return collection.median().clip(region)
