from typing import TypedDict, TypeAlias, NotRequired

class ImageTypeItem(TypedDict):
    id: str
    label: str
    description: str
    when_to_use: str
    icon: str
    is_optical: bool
    supported_galleries: list[str]


class ImageGalleryItem(TypedDict):
    id: str
    label: str
    max_area_km2: int
    start_date: str
    resolution_m: int


class ImageCompositionItem(TypedDict):
    id: str
    label: str

class TemporalConfigurationItem(TypedDict):
    id: str
    label: str
    months: int
    recommended: NotRequired[bool]

ImageType: TypeAlias = list[ImageTypeItem]
ImageGallery: TypeAlias = list[ImageGalleryItem]
ImageComposition: TypeAlias = list[ImageCompositionItem]
TemporalConfiguration: TypeAlias = list[TemporalConfigurationItem]
