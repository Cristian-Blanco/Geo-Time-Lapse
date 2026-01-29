from typing import TypedDict, TypeAlias

class ImageTypeItem(TypedDict):
    id: str
    label: str
    description: str
    when_to_use: str
    icon: str


class ImageGalleryItem(TypedDict):
    id: str
    label: str


class ImageCompositionItem(TypedDict):
    id: str
    label: str

ImageType: TypeAlias = list[ImageTypeItem]
ImageGallery: TypeAlias = list[ImageGalleryItem]
ImageComposition: TypeAlias = list[ImageCompositionItem]
