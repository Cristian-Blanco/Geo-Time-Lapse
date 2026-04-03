import ee

class ImageComposition:
    @staticmethod
    def build(
        collection: ee.ImageCollection,
        region: ee.Geometry,
    ) -> ee.Image:
        raise NotImplementedError
