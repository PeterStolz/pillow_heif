"""Test a built pi-heif-decoder wheel: assert the bundled native libraries, then run the suite.

Usage: pi-heif-wheel-test.py <project dir>

The expected libheif/libde265 versions are read from `libheif/build_libs.py`, so a
native-library bump only has to touch that file. The expected package version comes
from `PI_HEIF_VERSION`, set by the workflow.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

import pi_heif

PROJECT = Path(sys.argv[1])
build_libs = (PROJECT / "libheif" / "build_libs.py").read_text(encoding="utf-8")
expected_libheif = re.search(r"libheif-([0-9.]+)\.tar\.gz", build_libs).group(1)
expected_libde265 = re.search(r"libde265-([0-9.]+)\.tar\.gz", build_libs).group(1)

info = pi_heif.libheif_info()
print(info)
assert pi_heif.__version__ == os.environ["PI_HEIF_VERSION"], pi_heif.__version__
assert info["libheif"] == expected_libheif, f"libheif {info['libheif']} != {expected_libheif}"
assert f"version {expected_libde265}" in info["decoders"]["libde265"], info["decoders"]
# Decode-only build: no x265/aom encoders may sneak into the wheel (GPL).
assert info["encoders"] == {"mask": "mask"}, info["encoders"]
assert not info["HEIF"] and not info["AVIF"], info

# `test_full_build` asserts that an encoder is bundled, which is exactly what this build must not do.
subprocess.run([sys.executable, "-m", "pytest", str(PROJECT / "tests"), "-k", "not test_full_build"], check=True)
