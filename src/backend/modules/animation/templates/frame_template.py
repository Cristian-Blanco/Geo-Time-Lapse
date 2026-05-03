from PIL import Image, ImageFont, ImageDraw
from backend.domain.types.time_window import TimeWindow

class FrameTemplate:

    @staticmethod
    def apply(image: Image.Image, window: TimeWindow) -> Image.Image:
        raise NotImplementedError

    @staticmethod
    def apply_missing(window: TimeWindow, size: tuple[int, int] = (1920, 1080)) -> Image.Image:
        image = Image.new("RGB", size, (0, 0, 0))
        draw = ImageDraw.Draw(image)

        label = window["label"]

        try:
            font_main = ImageFont.truetype("arial.ttf", 50)
            font_label = ImageFont.truetype("arial.ttf", 30)
        except Exception:
            font_main = ImageFont.load_default()
            font_label = ImageFont.load_default()

        # text in the middle
        draw.text(
            (size[0] // 2, size[1] // 2),
            "Image not found",
            fill=(255, 255, 255),
            font=font_main,
            anchor="mm",
        )

        # text in the upper left corner
        draw.text((20, 20), label, fill=(255, 255, 255), font=font_label)

        return image
