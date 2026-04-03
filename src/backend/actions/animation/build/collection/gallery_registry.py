from .gallery import Gallery
from .sentinel_1_gallery import Sentinel1Gallery
from .sentinel_2_gallery import Sentinel2Gallery

class GalleryRegistry:

    _galleries: dict[str, Gallery] = {
        "sentinel_2": Sentinel2Gallery(),
        "sentinel_1": Sentinel1Gallery(),
    }

    @classmethod
    def get(cls, gallery_id: str) -> Gallery:
        return cls._galleries[gallery_id]
