import ee


def build_composed_image(
    composition_id: str,
    collection: ee.ImageCollection,
    start: ee.Date,
    end: ee.Date,
    region: ee.Geometry,
) -> ee.Image:
    filtered_collection = collection.filterDate(start, end)

    if composition_id == "mosaic":
        return filtered_collection.mosaic().clip(region)

    if composition_id == "single":
        return ee.Image(
            filtered_collection.sort("system:time_start").first()
        ).clip(region)

    if composition_id == "median":
        return filtered_collection.median().clip(region)

    raise ValueError(f"Unsupported composition: {composition_id}")
