import ee
from .image_composition import ImageComposition

class MosaicComposition(ImageComposition):
    @staticmethod
    def build(
        collection: ee.ImageCollection,
        region: ee.Geometry,
    ) -> ee.Image:
        return collection.mosaic().clip(region)
