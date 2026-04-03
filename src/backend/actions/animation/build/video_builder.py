from pathlib import Path
from moviepy import ImageSequenceClip

class VideoBuilder:

    @staticmethod
    def build(
        frames: list[Path],
        output_path: Path,
        frame_duration_seconds: int,
    ) -> Path:

        if not frames:
            raise RuntimeError("No frames provided")

        fps = 1 / frame_duration_seconds if frame_duration_seconds > 0 else 1

        clip = ImageSequenceClip([str(frame) for frame in frames], fps=fps)

        clip.write_videofile(str(output_path), codec="libx264")

        return output_path
