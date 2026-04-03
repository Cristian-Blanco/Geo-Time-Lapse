import ee
from .image_composition import ImageComposition

class SingleComposition(ImageComposition):
    @staticmethod
    def build(
        collection: ee.ImageCollection,
        region: ee.Geometry,
    ) -> ee.Image:
        return ee.Image(
            collection.sort("system:time_start").first()
        ).clip(region)
