from .image_composition import ImageComposition
from .mosaic_composition import MosaicComposition
from .single_composition import SingleComposition
from .median_composition import MedianComposition


class CompositionRegistry:
    _compositions: dict[str, type[ImageComposition]] = {
        "mosaic": MosaicComposition,
        "single": SingleComposition,
        "median": MedianComposition,
    }

    @classmethod
    def get(cls, composition_id: str) -> type[ImageComposition]:
        try:
            return cls._compositions[composition_id]
        except KeyError as error:
            raise ValueError(
                f"Unsupported composition: {composition_id}"
            ) from error
