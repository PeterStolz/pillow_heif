"""Transform the current pillow-heif source tree into pi-heif in place.

Usage: transform_to-pi_heif.py <version>

The version is the pi-heif-decoder release version (`<upstream>.postN`) that is
written into `_version.py`; it must start with the upstream version so the
Python code and the release line stay in sync.
"""

import re
import shutil
import sys
from pathlib import Path

if __name__ == "__main__":
    version = sys.argv[1]
    files = ["setup.py", "MANIFEST.in", "pillow_heif/_pillow_heif.c"]
    for directory in ("pillow_heif", "tests"):
        files.extend(str(path) for path in Path(directory).glob("*.py"))

    for filename in files:
        path = Path(filename)
        data = path.read_text(encoding="utf-8")
        path.write_text(data.replace("pillow_heif", "pi_heif"), encoding="utf-8")

    shutil.move("pillow_heif/_pillow_heif.c", "pillow_heif/_pi_heif.c")
    shutil.move("pillow_heif", "pi_heif")

    version_file = Path("pi_heif/_version.py")
    upstream = re.search(r'__version__\s*=\s*"(.*?)"', version_file.read_text(encoding="utf-8")).group(1)
    if not version.startswith(f"{upstream}.post"):
        raise SystemExit(f"{version} is not a post-release of upstream {upstream}")
    version_file.write_text(f'"""Version of pi_heif."""\n\n__version__ = "{version}"\n', encoding="utf-8")
