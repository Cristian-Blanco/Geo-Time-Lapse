from PIL import Image
from backend.domain.types.time_window import TimeWindow

class FrameTemplate:

    @staticmethod
    def apply(image: Image.Image, window: TimeWindow) -> Image.Image:
        raise NotImplementedError
