from backend.shared.result import Result
from backend.contracts.action import Action
from backend.contracts.types.animation_payload import AnimationPayload
from backend.domain.types.time_window import TimeWindow
from typing import Any

from backend.modules.animation.collection import CollectionRegistry, Gallery
from backend.modules.animation import (
    TemplateBuilder, FrameExporter, RegionBuilder, TimeWindowGenerator, VideoBuilder, VisualRangeResolver
)
from backend.shared.cancellation import raise_process_cancelled
from backend.shared.exceptions import ProcessCancelledError

import ee
from pathlib import Path

class BasicTimeLapseGeneration(Action[AnimationPayload, dict[str, Any]]):
    def invoke(self, payload: AnimationPayload) -> Result[dict[str, Any]]:
        try:

            progress = payload.get("progress_callback")
            is_cancelled = payload.get("is_cancelled")

            progress(10, "Preparing export")
            raise_process_cancelled(is_cancelled)

            # Initialize Earth Engine session
            ee.Initialize(project=payload["project_id"])

            # Build region of interest from input coordinates
            progress(15, "Creating image")
            raise_process_cancelled(is_cancelled)
            region: ee.Geometry = RegionBuilder.from_coordinates(payload["coordinates"])

            # Resolve gallery and build filtered image collection
            progress(20, "Requesting Google imagery")
            raise_process_cancelled(is_cancelled)
            gallery: Gallery = CollectionRegistry.get(payload["gallery_id"])
            collection: ee.ImageCollection = gallery.build_collection(
                start_date=payload["start_date"],
                end_date=payload["end_date"],
                region=region,
                cloud_percentage=payload["cloud_percentage"]
            )

            progress(35, "Building time windows")
            raise_process_cancelled(is_cancelled)
            windows: list[TimeWindow] = TimeWindowGenerator.generate(
                start_date=payload["start_date"],
                end_date=payload["end_date"],
                interval_months=payload["temporal_interval_months"],
            )
            
            # Dynamic metadata injection (key adjustment)
            

            # 1. Satellite mapping based on selected gallery
            satellite_map = {
                "sentinel_2": "Sentinel-2",
                "sentinel_1": "Sentinel-1",
                "landsat_8": "Landsat 8",
                "landsat_9": "Landsat 9"
            }

            # 2. Determine satellite name from user selection
            satellite_name = satellite_map.get(payload["gallery_id"], "Desconocido")

            # 3. Define composition method (e.g., median, mosaic)
            composition_method = payload.get("composition", "median")

            # 4. Inject metadata into each time window
            for w in windows:
                # Default CRS used by Earth Engine
                w["crs"] = "EPSG:4326"

                # Assign satellite dynamically
                w["satellite"] = satellite_name

                # Define image identifier based on composition method
                # Example: median_2024-03_2025-03
                w["image_id"] = f"{composition_method}_{w['label']}"


            # Robust bounding box extraction
            coords = payload["coordinates"]

            print("COORDINATES RAW:", coords)

            # Case 1: direct bounding box [xmin, ymin, xmax, ymax]
            if isinstance(coords, list) and len(coords) == 4 and all(isinstance(x, (int, float)) for x in coords):
                bbox = tuple(coords)

            # Case 2: polygon / GeoJSON structure
            else:
                def flatten_coords(c):
                    while isinstance(c[0], list):
                        c = c[0]
                    return c

                coords = flatten_coords(coords)

                if not isinstance(coords[0], (list, tuple)) or len(coords[0]) < 2:
                    raise ValueError(f"Coordenadas inválidas: {coords}")

                xs = [p[0] for p in coords]
                ys = [p[1] for p in coords]

                bbox = (min(xs), min(ys), max(xs), max(ys))

            print("BBOX FINAL:", bbox)

            # Assign bounding box to each time window
            for w in windows:
                w["bbox"] = bbox

            print("WINDOW SAMPLE:", windows[0])

            # Visualization configuration
            progress(40, "Configuring bands")
            raise_process_cancelled(is_cancelled)

            vis_params = VisualRangeResolver.resolve(
                collection=collection,
                region=region,
                gallery_id=payload["gallery_id"],
                image_type=payload["image_type"],
                normalize_images=payload["check_normalize_images"],
                is_optical=gallery.is_optical,
            )

            # Frame export
            progress(50, "Downloading frames")
            raise_process_cancelled(is_cancelled)

            output_dir = Path(payload["output_dir"])
            frames_dir = output_dir / "frames"

            frame_exporter = FrameExporter(
                composition_id=payload["composition"],
                vis_params=vis_params,
                output_dir=frames_dir
            )

            frame_paths: list[Path | None] = frame_exporter.export(
                collection=collection,
                windows=windows,
                region=region,
                progress_callback=progress
            )

            # Template application
            progress(85, "Applying template")
            raise_process_cancelled(is_cancelled)

            templated_frames: list[Path] = TemplateBuilder.apply(
                frames=frame_paths,
                windows=windows,
                template_id=payload["template"],
                output_dir=frames_dir,
            )

            # Video generation
            progress(90, "Building video")
            raise_process_cancelled(is_cancelled)

            video_path: Path = VideoBuilder.build(
                frames=templated_frames,
                output_path=output_dir / "timelapse.mp4",
                frame_duration_seconds=payload["frame_duration_seconds"],
            )

            progress(100, "Completed")

            return Result.success({
                "video_path": str(video_path)
            })

        except ProcessCancelledError as error:
            return Result.fail(str(error))

        except Exception as error:
            print("❌ ERROR FINAL:", error)
            return Result.fail(str(error))