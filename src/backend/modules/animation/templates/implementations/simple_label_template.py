from PIL import ImageDraw, ImageFont, Image
from backend.domain.types.time_window import TimeWindow
from ..frame_template import FrameTemplate

class SimpleLabelTemplate(FrameTemplate):

    @staticmethod
    def apply(image: Image.Image, window: TimeWindow) -> Image.Image:
        draw = ImageDraw.Draw(image)

        text = window["label"]

        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except OSError:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        padding = 10

        draw.rectangle(
            [
                (10 - padding, 10 - padding),
                (10 + text_width + padding, 10 + text_height + padding),
            ],
            fill=(0, 0, 0)
        )

        draw.text((10, 10), text, fill=(255, 255, 255), font=font)

        return image
