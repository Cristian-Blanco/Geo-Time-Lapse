from frontend.domain.imagery.types import ImageComposition, ImageGallery, ImageType

IMAGE_TYPES: ImageType = [
    {
        "id": "natural",
        "label": "Natural color",
        "description": "Best for general visualization",
        "when_to_use": (
            "Ideal for areas with low cloud cover "
            "and for general visual comparison"
        ),
        "icon": "natural_color.png",
    },
    {
        "id": "infrared",
        "label": "Infrared",
        "description": "Vegetation, soil, and land cover changes",
        "when_to_use": (
            "Useful for analyzing vegetation vigor, water stress, "
            "and soil changes"
        ),
        "icon": "false_color.png",
    },
    {
        "id": "radar",
        "label": "Radar",
        "description": "High cloud cover regions",
        "when_to_use": (
            "Recommended for areas with persistent cloud cover "
            "or for structural analysis"
        ),
        "icon": "radar_filter.png",
    },
]

IMAGE_GALLERIES: ImageGallery = [
    {"id": "sentinel", "label": "Sentinel"},
    {"id": "landsat", "label": "Landsat"},
]

IMAGE_COMPOSITIONS: ImageComposition = [
    {"id": "mosaic", "label": "Image mosaic"},
    {"id": "single", "label": "Single image"},
]
