from frontend.helpers.parsing import parse_float
from .validators import is_valid_bbox

def normalize_bbox(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> tuple[float, float, float, float]:
    xmin = min(lon1, lon2)
    xmax = max(lon1, lon2)
    ymin = min(lat1, lat2)
    ymax = max(lat1, lat2)

    return xmin, ymin, xmax, ymax

def get_valid_bbox_from_strings(
    lat1_str: str,
    lon1_str: str,
    lat2_str: str,
    lon2_str: str,
) -> tuple[float, float, float, float] | None:
    lat1 = parse_float(lat1_str)
    lon1 = parse_float(lon1_str)
    lat2 = parse_float(lat2_str)
    lon2 = parse_float(lon2_str)

    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return None

    if not is_valid_bbox(lat1, lon1, lat2, lon2):
        return None

    return normalize_bbox(lat1, lon1, lat2, lon2)
