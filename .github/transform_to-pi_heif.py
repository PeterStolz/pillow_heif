"""Transform the current pillow-heif source tree into pi-heif in place."""

import shutil
from pathlib import Path

if __name__ == "__main__":
    files = ["setup.py", "MANIFEST.in", "pillow_heif/_pillow_heif.c"]
    for directory in ("pillow_heif", "tests"):
        files.extend(str(path) for path in Path(directory).glob("*.py"))

    for filename in files:
        path = Path(filename)
        data = path.read_text(encoding="utf-8")
        path.write_text(data.replace("pillow_heif", "pi_heif"), encoding="utf-8")

    shutil.move("pillow_heif/_pillow_heif.c", "pillow_heif/_pi_heif.c")
    shutil.move("pillow_heif", "pi_heif")
