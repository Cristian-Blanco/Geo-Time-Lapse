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
        "supports_cloud_filter": True,
        "supported_galleries": ["sentinel", "landsat"], # The name in support_galleries must be equal to the id in IMAGE_GALLERIES
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
        "supports_cloud_filter": True,
        "supported_galleries": ["sentinel", "landsat"],
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
        "supports_cloud_filter": False,
        "supported_galleries": ["sentinel"],
    },
]

IMAGE_GALLERIES: ImageGallery = [
    {
        "id": "sentinel",
        "label": "Sentinel",
        "max_area_km2": 100,
    },
    {
        "id": "landsat",
        "label": "Landsat",
        "max_area_km2": 200
    },
]

IMAGE_COMPOSITIONS: ImageComposition = [
    {"id": "mosaic", "label": "Image mosaic"},
    {"id": "single", "label": "Single image"},
]
