import ee

class Gallery:

    collection_id: str
    sensor_type: str
    cloud_property: str | None

    def build_collection(
        self,
        start_date: str,
        end_date: str,
        region: ee.Geometry,
        cloud_percentage: int | None,
    ) -> ee.ImageCollection:

        collection = (
            ee.ImageCollection(self.collection_id)
            .filterDate(start_date, end_date)
            .filterBounds(region)
        )

        if self.cloud_property and cloud_percentage:
            collection = collection.filter(
                ee.Filter.lt(self.cloud_property, cloud_percentage)
            )

        return collection
