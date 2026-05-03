from PIL import ImageDraw, ImageFont, Image
from pathlib import Path
from backend.domain.types.time_window import TimeWindow
from ..frame_template import FrameTemplate
import math


class AdvancedMapTemplate(FrameTemplate):

    @staticmethod
    def apply(image: Image.Image, window: TimeWindow) -> Image.Image:

        # Font configuration
        try:
            font_big = ImageFont.truetype("arial.ttf", 32)
            font_small = ImageFont.truetype("arial.ttf", 16)
        except:
            font_big = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # White margin layout (all sides)
        original_w, original_h = image.size
        margin = 80

        canvas = Image.new(
            "RGB",
            (original_w + margin * 2, original_h + margin * 2),
            (255, 255, 255)
        )

        canvas.paste(image, (margin, margin))

        image = canvas
        draw = ImageDraw.Draw(image)

        w, h = image.size

        # Map drawing area
        map_xmin = margin
        map_xmax = margin + original_w
        map_ymin = margin
        map_ymax = margin + original_h

        # Draw map frame
        draw.rectangle(
            (map_xmin, map_ymin, map_xmax, map_ymax),
            outline=(0, 0, 0),
            width=2
        )

        # Label (top-left inside map)
        text = window.get("label", "Sin fecha")

        bbox_text = draw.textbbox((0, 0), text, font=font_big)
        tw = bbox_text[2] - bbox_text[0]
        th = bbox_text[3] - bbox_text[1]

        pad = 8

        draw.rectangle(
            (
                map_xmin + 10,
                map_ymin + 10,
                map_xmin + 10 + tw + pad * 2,
                map_ymin + 10 + th + pad * 2
            ),
            fill=(255, 255, 255),
            outline=(0, 0, 0)
        )

        draw.text(
            (map_xmin + 10 + pad, map_ymin + 10 + pad),
            text,
            fill=(0, 0, 0),
            font=font_big
        )

        # North arrow
        try:
            base = Path(__file__).resolve()
            while base.name != "src":
                base = base.parent

            north_path = base / "frontend/presentation/resources/icons/north_arrow.png"

            north = Image.open(north_path).convert("RGBA")
            north = north.resize((120, 120))

            image.paste(north, (map_xmax - 140, map_ymin + 20), north)

        except Exception as e:
            print("No se pudo cargar norte:", e)

        # Geographic grid and coordinates
        bbox = window.get("bbox")

        if bbox:
            xmin, ymin, xmax, ymax = bbox

            lon_range = xmax - xmin
            lat_range = ymax - ymin

            steps = 5
            grid_color = (0, 0, 0, 60)

            # Longitude lines and labels
            for i in range(steps + 1):
                lon = xmin + i * (lon_range / steps)

                px = int((lon - xmin) / lon_range * original_w + map_xmin)

                draw.line((px, map_ymin, px, map_ymax), fill=grid_color)

                label = f"{lon:.4f}"

                # Bottom labels
                draw.text((px - 20, map_ymax + 5), label, fill=(0, 0, 0), font=font_small)

                # Top labels
                draw.text((px - 20, map_ymin - 20), label, fill=(0, 0, 0), font=font_small)

            # Latitude lines and labels
            for j in range(steps + 1):
                lat = ymin + j * (lat_range / steps)

                py = int(map_ymax - ((lat - ymin) / lat_range * original_h))

                draw.line((map_xmin, py, map_xmax, py), fill=grid_color)

                label = f"{lat:.4f}"

                txt_img = Image.new("RGBA", (100, 30), (255, 255, 255, 255))
                txt_draw = ImageDraw.Draw(txt_img)
                txt_draw.text((5, 5), label, fill=(0, 0, 0), font=font_small)

                txt_img = txt_img.rotate(90, expand=True)

                # Left labels
                image.paste(
                    txt_img,
                    (map_xmin - txt_img.width - 5, py - txt_img.height // 2),
                    txt_img
                )

                # Right labels
                image.paste(
                    txt_img,
                    (map_xmax + 5, py - txt_img.height // 2),
                    txt_img
                )

        # Scale bar (inside map)
        if bbox:
            lat_mid = (ymin + ymax) / 2
            meters_per_degree = 111320 * math.cos(math.radians(lat_mid))

            width_m = (xmax - xmin) * meters_per_degree
            meters_per_pixel = width_m / original_w

            scale_m = width_m / 5
            scale_px = int(scale_m / meters_per_pixel)

            x = map_xmin + 20
            y = map_ymax - 50

            draw.rectangle(
                (x - 10, y - 25, x + scale_px + 10, y + 30),
                fill=(255, 255, 255),
                outline=(0, 0, 0)
            )

            half = scale_px // 2

            draw.rectangle((x, y, x + half, y + 10), fill=(0, 0, 0))
            draw.rectangle((x + half, y, x + scale_px, y + 10),
                           fill=(255, 255, 255), outline=(0, 0, 0))

            draw.text((x, y + 12), "0", fill=(0, 0, 0), font=font_small)
            draw.text((x + half - 10, y + 12),
                      f"{int(scale_m/2)}", fill=(0, 0, 0), font=font_small)

            label = f"{int(scale_m)} m" if scale_m < 1000 else f"{scale_m/1000:.1f} km"

            draw.text((x + scale_px - 40, y + 12),
                      label, fill=(0, 0, 0), font=font_small)

        # Metadata text (bottom area)
        crs = window.get("crs", "CRS desconocido")
        image_id = window.get("image_id", "ID desconocido")
        satellite = window.get("satellite", "Satélite desconocido")

        meta_text = f"CRS: {crs} | ID: {image_id} | Fuente: {satellite}"

        bbox_meta = draw.textbbox((0, 0), meta_text, font=font_small)
        tw = bbox_meta[2] - bbox_meta[0]
        th = bbox_meta[3] - bbox_meta[1]

        x_meta = map_xmin
        y_meta = map_ymax + 40

        draw.text(
            (x_meta, y_meta),
            meta_text,
            fill=(0, 0, 0),
            font=font_small
        )

        return image