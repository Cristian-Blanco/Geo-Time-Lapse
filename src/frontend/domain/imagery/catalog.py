from frontend.domain.imagery.satellite import IMAGE_TYPES, IMAGE_GALLERIES, TEMPORAL_CONFIGURATIONS
from frontend.domain.imagery.types import TemporalConfigurationItem

class Catalog:
    @staticmethod
    def get_image_type_label(image_type_id: str | None) -> str | None:
        if not image_type_id:
            return None

        for image_type in IMAGE_TYPES:
            if image_type["id"] == image_type_id:
                return image_type["label"]

        return None

    @staticmethod
    def get_gallery_label(gallery_id: str | None) -> str | None:
        if not gallery_id:
            return None

        for gallery in IMAGE_GALLERIES:
            if gallery["id"] == gallery_id:
                return gallery["label"]

        return None

    @staticmethod
    def get_gallery_start_date(gallery_id: str | None) -> str | None:
        if not gallery_id:
            return None

        for gallery in IMAGE_GALLERIES:
            if gallery["id"] == gallery_id:
                return gallery.get("start_date")

        return None

    @staticmethod
    def get_recommended_temporal_configuration() -> TemporalConfigurationItem:
        recommended_items = [
            item for item in TEMPORAL_CONFIGURATIONS
            if item.get("recommended", False)
        ]

        if len(recommended_items) > 1:
            raise ValueError("Only one temporal configuration can be marked as recommended.")

        return recommended_items[0]
