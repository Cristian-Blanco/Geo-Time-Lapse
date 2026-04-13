from typing import TypedDict, NotRequired

class ImageTypeDefinition(TypedDict):
    bands: list[str]
    vis_min: list[float] | float
    vis_max: list[float] | float
    scale: NotRequired[int]
