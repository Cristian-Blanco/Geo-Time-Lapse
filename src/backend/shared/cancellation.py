from collections.abc import Callable
from backend.shared.exceptions import ProcessCancelledError

def raise_process_cancelled(is_cancelled: Callable[[], bool] | None) -> None:
    if is_cancelled is not None and is_cancelled():
        raise ProcessCancelledError("Process cancelled")
