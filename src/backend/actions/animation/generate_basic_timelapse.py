from backend.shared.result import Result
from backend.contracts.action import Action
from backend.contracts.types.animation_payload import AnimationPayload
from backend.domain.types.time_window import TimeWindow
from typing import Any

from backend.modules.animation.collection import CollectionRegistry, Gallery
from backend.modules.animation import (
    CreateTemplate, FrameExporter, RegionBuilder, TimeWindowGenerator, VideoBuilder
)

import ee
from pathlib import Path

class GenerateBasicTimelapse(Action[AnimationPayload, dict[str, Any]]):
    def invoke(self, payload: AnimationPayload) -> Result[dict[str, Any]]:
        try:

            progress = payload.get("progress_callback")
            is_cancelled = payload.get("is_cancelled")

            progress(10, "Preparing export")

            if is_cancelled and is_cancelled():
                return Result.fail("It's cancelled")

            # Initialize Earth Engine session
            ee.Initialize(project=payload["project_id"])

            # Build region of interest from input coordinates
            progress(25, "Creating image")
            region: ee.Geometry = RegionBuilder.from_coordinates(payload["coordinates"])

            # Resolve gallery and build filtered image collection
            progress(30, "Requesting Google imagery")
            gallery: Gallery = CollectionRegistry.get(payload["gallery_id"])
            collection: ee.ImageCollection = gallery.build_collection(
                start_date=payload["start_date"],
                end_date=payload["end_date"],
                region=region,
                cloud_percentage=payload["cloud_percentage"]

            )

            # Generate temporal windows for frame extraction
            progress(40, "Building time windows")
            windows: list[TimeWindow] = TimeWindowGenerator.generate(
                start_date=payload["start_date"],
                end_date=payload["end_date"],
                interval_months=payload["temporal_interval_months"],
            )

            # Prepare output directories
            progress(50, "Downloading JPG frames")
            output_dir = Path(payload["output_dir"])
            frames_dir = output_dir / "frames"

            # Export frames from collection using selected configuration
            frame_exporter = FrameExporter(
                composition_id=payload["composition"],
                gallery_id=payload["gallery_id"],
                image_type=payload["image_type"],
                output_dir=frames_dir
            )
            frame_paths: list[Path] = frame_exporter.export(
                collection=collection,
                windows=windows,
                region=region,
                progress_callback=progress
            )

            # Apply visual template to each frame (labels, overlays)
            progress(85, "Creating template")
            templated_frames: list[Path] = CreateTemplate.apply(
                    frames=frame_paths,
                    windows=windows,
                    template_id=payload["template"],
                    output_dir=frames_dir,
                )

            # Build final video from processed frames
            progress(90, "Building video")
            video_path: Path = VideoBuilder.build(
                frames=templated_frames,
                output_path=output_dir / "timelapse.mp4",
                frame_duration_seconds=payload["frame_duration_seconds"],
            )

            progress(100, "Completed")
            return Result.success({
                "video_path": str(video_path)
            })

        except Exception as error:
            return Result.fail(str(error))
