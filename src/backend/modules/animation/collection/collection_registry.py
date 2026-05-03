from .gallery import Gallery
from .implementations import (
    Sentinel1Gallery, Sentinel2Gallery
)

class CollectionRegistry:

    _galleries: dict[str, Gallery] = {
        "sentinel_2": Sentinel2Gallery(),
        "sentinel_1": Sentinel1Gallery(),
    }

    @classmethod
    def get(cls, gallery_id: str) -> Gallery:
        return cls._galleries[gallery_id]
