from .gallery import Gallery

class Sentinel2Gallery(Gallery):
    collection_id = "COPERNICUS/S2_SR_HARMONIZED"
    sensor_type = "optical"
    cloud_property = "CLOUDY_PIXEL_PERCENTAGE"
