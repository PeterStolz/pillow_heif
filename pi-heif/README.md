# pi-heif-decoder

**A maintenance fork that continues the discontinued decode-only `pi-heif`
package with up-to-date native libraries.**

[![Decoder wheels](https://github.com/PeterStolz/pillow_heif/actions/workflows/pi-heif-decoder-artifacts.yml/badge.svg?branch=pi-heif)](https://github.com/PeterStolz/pillow_heif/actions/workflows/pi-heif-decoder-artifacts.yml)
![pypi](https://img.shields.io/pypi/v/pi-heif-decoder.svg)
![python](https://img.shields.io/badge/python-3.13-blue)

## Why this fork exists

`pi-heif` was the decode-only, encoder-free variant of
[pillow-heif](https://github.com/bigcat88/pillow_heif). Upstream discontinued it
in [bigcat88/pillow_heif#431](https://github.com/bigcat88/pillow_heif/pull/431);
its final release, `pi-heif 1.4.0`, ships wheels that bundle **libheif 1.23.0**.

In August/September 2026 the [HEIF Heist](https://heif-heist.com/) research
disclosed a family of memory-safety bugs in libheif and libde265 — the native
decoders underneath `pi-heif`, `pillow-heif`, ImageMagick, libvips and others —
that were used for remote code execution via uploaded images. libheif 1.23.0 sits
inside the affected ranges of several of those advisories (fixed in libheif
1.23.2 → 1.23.4, libde265 1.1.2 → 1.1.3).

Because the wheel bundles its own copy of libheif, a patched system package does
**not** help: the Python process loads the vulnerable library from the wheel. And
because SBOM/CVE scanners such as Trivy and Dependency-Track do not inventory
native libraries inside wheels, the exposure is invisible to them.

Switching to `pillow-heif` proper fixes the libheif version but pulls in the
GPL-licensed x265 encoder, which is exactly what `pi-heif` existed to avoid.

This fork keeps the decode-only, permissively-licensed wheel and tracks current
upstream releases of both the Python code and the native libraries.

## What you get

| | |
|---|---|
| Distribution name | `pi-heif-decoder` |
| Import name | `pi_heif` (drop-in for the discontinued `pi-heif`) |
| Python | CPython 3.13 |
| Wheels | manylinux x86_64, manylinux aarch64, macOS arm64, Windows x64 |
| libheif | 1.23.4 |
| libde265 | 1.1.3 |
| Encoders | none (only the built-in `mask` pseudo-encoder is reported) |
| Decoders | HEVC via libde265 — no AV1/AVIF decoder is bundled; use Pillow's own AVIF support |

Each wheel build asserts the bundled libheif/libde265 versions and the absence of
real encoders before it is published.

## Versioning and release process

Releases follow upstream pillow-heif: the fork's `pi-heif` branch is a small
patch series rebased onto the latest upstream tag, and the package version is
`<upstream version>.postN`.

- upstream `v1.7.0` → `pi-heif-decoder 1.7.0.postN`
- fork-only changes (e.g. a native-library security bump) increment `postN`
- a new upstream release resets to `.post1` after the rebase

Wheels are built on GitHub-hosted runners and published with
[PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (OIDC) —
there is no long-lived PyPI token anywhere in this repository. The publishing job
runs only for `pi-heif-decoder-v*` tags and requires a manual environment
approval. Native source tarballs are pinned by SHA-256 in `libheif/build_libs.py`.

## Install

```console
python3 -m pip install -U pi-heif-decoder
```

If you migrate from `pi-heif`, uninstall it first — both provide the `pi_heif`
import:

```console
python3 -m pip uninstall pi-heif
python3 -m pip install pi-heif-decoder
```

## Usage

The API is pillow-heif's minus `save`. Refer to the
[pillow-heif docs](https://pillow-heif.readthedocs.io/).

### As a Pillow plugin

```python
from PIL import Image
from pi_heif import register_heif_opener

register_heif_opener()

im = Image.open("images/input.heic")  # do whatever you need with a Pillow image
im.show()
```

### Verify what is actually loaded

```python
import pi_heif

info = pi_heif.libheif_info()
assert info["libheif"] == "1.23.4"
assert "version 1.1.3" in info["decoders"]["libde265"]
assert info["encoders"] == {"mask": "mask"}
```

### Decoded image data as a NumPy array

```python
import numpy as np
import pi_heif

if pi_heif.is_supported("input.heic"):
    heif_file = pi_heif.open_heif("input.heic")
    np_array = np.asarray(heif_file)
```

## License boundary

The wheel contains the BSD-3-Clause Python extension plus dynamically linked,
LGPL-3.0 libheif and libde265. Source and license locations for the bundled
libraries are recorded in `LICENSES_bundled.txt` inside the distribution.
No GPL components (x265, x264, …) are built or shipped.
