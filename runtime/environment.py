from pathlib import Path
import sys

PLUGIN_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = PLUGIN_DIR / "src"

def setup_runtime():
    if str(SRC_DIR) not in sys.path:
        sys.path.insert(0, str(SRC_DIR))
    return PLUGIN_DIR
