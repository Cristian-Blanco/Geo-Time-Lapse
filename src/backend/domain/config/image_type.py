from backend.domain.types.image_type_config import ImageTypeDefinition

IMAGE_TYPES: dict[str, dict[str, ImageTypeDefinition]] = {
    "sentinel_2": {
        "natural": {
            "bands": ["B4", "B3", "B2"],
            "vis_min": 0.0,
            "vis_max": 3000.0,
            "scale": 10
        },
        "infrared": {
            "bands": ["B8", "B4", "B3"],
            "vis_min": 0.0,
            "vis_max": 3000.0,
            "scale": 10
        },
    },
    "sentinel_1": {
        "radar": {
            "bands": ["VV"],
            "vis_min": -25.0,
            "vis_max": 5.0,
            "scale": 30
        },
    },
}
