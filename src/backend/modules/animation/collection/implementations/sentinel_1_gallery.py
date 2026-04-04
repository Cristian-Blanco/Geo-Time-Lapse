from ..gallery import Gallery

class Sentinel1Gallery(Gallery):
    collection_id = "COPERNICUS/S1_GRD"
    sensor_type = "radar"
    cloud_property = None
