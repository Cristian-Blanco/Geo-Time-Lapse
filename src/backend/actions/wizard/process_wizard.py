from backend.shared.result import Result
from backend.contracts.action import Action
from typing import TypedDict, Any, NotRequired
from collections.abc import Callable
import time

class AnimationPayload(TypedDict):
    mode: str
    output_dir: str
    progress_callback: NotRequired[Callable[[int, str], None]]
    is_cancelled: NotRequired[Callable[[], bool]]

class ProcessWizardAction(Action[AnimationPayload, dict[str, Any]]):
    def invoke(self, payload: AnimationPayload) -> Result[dict[str, Any]]:
        progress = payload.get("progress_callback")
        is_cancelled = payload.get("is_cancelled")

        steps = [
            (10, "Preparing export..."),
            (25, "Requesting Google imagery..."),
            (50, "Downloading JPG frames..."),
            (70, "Download complete..."),
            (80, "Building animation..."),
            (95, "Finalizing output..."),
            (100, "Completed"),
        ]

        for percent, message in steps:
            if is_cancelled and is_cancelled():
                return Result.fail("It's cancelled")

            if progress:
                progress(percent, message)

            time.sleep(1)

        return Result.success({"ok": True})
