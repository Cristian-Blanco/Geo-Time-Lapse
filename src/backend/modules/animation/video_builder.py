from pathlib import Path
import subprocess
import imageio_ffmpeg
import os

class VideoBuilder:

    @staticmethod
    def build(
        frames: list[Path],
        output_path: Path,
        frame_duration_seconds: int,
    ) -> Path:

        if not frames:
            raise RuntimeError("No frames provided")

        if frame_duration_seconds <= 0:
            frame_duration_seconds = 1

        output_path = output_path.with_suffix(".mp4")

        # Get ffmpeg version in the SO
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

        concat_file = output_path.with_suffix(".txt")

        try:
            # Save everything to a text file so that FFmpeg can read it
            with concat_file.open("w", encoding="utf-8") as file:
                for frame in frames:
                    frame_path = str(frame.resolve()).replace("\\", "/")
                    file.write(f"file '{frame_path}'\n")
                    file.write(f"duration {frame_duration_seconds}\n")

                # FFmpeg needs to repeat the last frame to match the final duration
                last_frame = str(frames[-1].resolve()).replace("\\", "/")
                file.write(f"file '{last_frame}'\n")

            # Hide the FFmpeg console window on Windows
            startupinfo = None
            creationflags = 0

            # Check if the operating system is Windows.
            if os.name == "nt":
                startupinfo = subprocess.STARTUPINFO() # type: ignore[attr-defined]
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW # type: ignore[attr-defined]
                creationflags = subprocess.CREATE_NO_WINDOW # type: ignore[attr-defined]

            command = [
                ffmpeg_exe,
                "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_file),

                # If the width is odd, add 1 pixel.
                # If the height is odd, add 1 pixel.
                "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
                "-pix_fmt", "yuv420p",
                str(output_path),
            ]

            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                startupinfo=startupinfo,
                creationflags=creationflags,
            )

            if result.returncode != 0:
                raise RuntimeError(f"FFmpeg failed: {result.stderr}")

            return output_path

        finally:
            concat_file.unlink(missing_ok=True) # Remove txt file
