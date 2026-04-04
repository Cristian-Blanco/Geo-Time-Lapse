import ee

class RegionBuilder:

    @staticmethod
    def from_coordinates(coordinates: list[float]) -> ee.Geometry:
        min_lon, min_lat, max_lon, max_lat = coordinates
        return ee.Geometry.Rectangle([min_lon, min_lat, max_lon, max_lat])
