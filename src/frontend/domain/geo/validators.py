from .constants import (
    MIN_LATITUDE,
    MAX_LATITUDE,
    MIN_LONGITUDE,
    MAX_LONGITUDE,
)

def is_valid_lat(lat: float) -> bool:
    return MIN_LATITUDE <= lat <= MAX_LATITUDE

def is_valid_lon(lon: float) -> bool:
    return MIN_LONGITUDE <= lon <= MAX_LONGITUDE

def is_valid_bbox(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> bool:
    if not (is_valid_lat(lat1) and is_valid_lat(lat2)):
        return False

    if not (is_valid_lon(lon1) and is_valid_lon(lon2)):
        return False

    # Avoid a degenerate rectangle
    if lat1 == lat2 or lon1 == lon2:
        return False

    return True
