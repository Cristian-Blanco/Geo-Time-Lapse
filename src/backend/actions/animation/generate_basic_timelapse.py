from backend.shared.result import Result
from backend.contracts.action import Action
from backend.contracts.types.animation_payload import AnimationPayload
from typing import Any

from .build.region_builder import RegionBuilder
from .build.time_windows_generator import TimeWindowGenerator
from .build.collection.gallery_registry import GalleryRegistry

from .build.frame_exporter import FrameExporter
from .build.create_template import CreateTemplate
from .build.video_builder import VideoBuilder

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

            ee.Initialize(project=payload["project_id"])

            progress(25, "creating image")
            region = RegionBuilder.from_coordinates(payload["coordinates"])

            progress(30, "Requesting Google imagery")
            gallery = GalleryRegistry.get(payload["gallery_id"])
            collection = gallery.build_collection(
                start_date=payload["start_date"],
                end_date=payload["end_date"],
                region=region,
                cloud_percentage=payload["cloud_percentage"]

            )

            progress(40, "Building time windows")
            windows = TimeWindowGenerator.generate(
                start_date=payload["start_date"],
                end_date=payload["end_date"],
                interval_months=payload["temporal_interval_months"],
            )

            progress(50, "Get frames")

            output_dir = Path(payload["output_dir"])
            frames_dir = output_dir / "frames"

            frame_paths = FrameExporter.export(
                collection=collection,
                windows=windows,
                region=region,
                output_dir=frames_dir,
                composition=payload["composition"],
                gallery_id=payload["gallery_id"],
                image_type=payload["image_type"],
                progress_callback=progress
            )

            progress(85, "Creating templates")
            templated_frames = CreateTemplate.apply(
                    frames=frame_paths,
                    windows=windows,
                    template_id=payload["template"],
                    output_dir=frames_dir,
                )

            progress(90, "Building video")
            video_path = VideoBuilder.build(
                frames=templated_frames,
                output_path=output_dir / "timelapse.mp4",
                frame_duration_seconds=payload["frame_duration_seconds"],
            )

            progress(100, "Completed")
            return Result.success({
                "video_path": video_path
            })

        except Exception as error:
            return Result.fail(str(error))
