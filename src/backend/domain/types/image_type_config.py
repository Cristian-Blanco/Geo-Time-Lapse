from typing import TypedDict

class ImageTypeDefinition(TypedDict):
    bands: list[str]
    vis_min: int | float
    vis_max: int | float
