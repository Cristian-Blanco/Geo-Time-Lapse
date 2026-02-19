from typing import TypedDict, TypeAlias

class ImageTypeItem(TypedDict):
    id: str
    label: str
    description: str
    when_to_use: str
    icon: str
    supports_cloud_filter: bool
    supported_galleries: list[str]


class ImageGalleryItem(TypedDict):
    id: str
    label: str
    max_area_km2: int


class ImageCompositionItem(TypedDict):
    id: str
    label: str

ImageType: TypeAlias = list[ImageTypeItem]
ImageGallery: TypeAlias = list[ImageGalleryItem]
ImageComposition: TypeAlias = list[ImageCompositionItem]
