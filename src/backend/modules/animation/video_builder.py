from pathlib import Path
import subprocess
import imageio_ffmpeg


class VideoBuilder:

    @staticmethod
    def build(
        frames: list[Path],
        output_path: Path,
        frame_duration_seconds: int,
    ) -> Path:

        print(">>> ENTRÓ A VIDEO BUILDER")

        if not frames:
            raise RuntimeError("No frames provided")

        # 🔥 ordenar frames
        frames = sorted(frames, key=lambda x: x.name)

        print("Frames encontrados:", len(frames))
        print("Primer frame:", frames[0])

        # 📂 carpeta de frames
        frames_dir = frames[0].parent

        # 📄 archivo temporal para ffmpeg
        list_file = frames_dir / "frames.txt"

        print(">>> CREANDO LISTA DE FRAMES")

        with open(list_file, "w", encoding="utf-8") as f:
            for frame in frames:
                f.write(f"file '{frame.as_posix()}'\n")
                f.write(f"duration {frame_duration_seconds}\n")

            # ⚠️ necesario para que el último frame se vea
            f.write(f"file '{frames[-1].as_posix()}'\n")

        # 🔧 ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        print("FFMPEG:", ffmpeg_path)

        # 🔥 COMANDO CORRECTO
        cmd = [
            ffmpeg_path,
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(list_file),
            "-vsync", "vfr",
            "-pix_fmt", "yuv420p",
            "-c:v", "libx264",
            str(output_path)
        ]

        print("CMD:", " ".join(cmd))

        result = subprocess.run(cmd, capture_output=True, text=True)

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode != 0:
            raise RuntimeError("FFMPEG falló")

        print(">>> VIDEO GENERADO:", output_path)

        return output_path