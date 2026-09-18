# pi-heif decoder-only maintenance fork

This branch continues the decoder-only `pi-heif` package after upstream
discontinued it in [PR #431](https://github.com/bigcat88/pillow_heif/pull/431).
The pi-heif-specific changes are maintained as a small patch series on top of
the latest stable pillow-heif release (currently `v1.7.0`) so fixes and features
can continue to flow from upstream. It builds against a current, decoder-only
libheif without GPL encoders.

Linux wheels bundle only decoder-capable libheif and libde265. They do not build
or ship x265, x264, AOM, dav1d, OpenH264, or encoder plugins.

[![Decoder artifacts](https://github.com/PeterStolz/pillow_heif/actions/workflows/pi-heif-decoder-artifacts.yml/badge.svg?branch=pi-heif)](https://github.com/PeterStolz/pillow_heif/actions/workflows/pi-heif-decoder-artifacts.yml)

![PythonVersion](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)
![impl](https://img.shields.io/pypi/implementation/pi-heif-decoder)
![pypi](https://img.shields.io/pypi/v/pi-heif-decoder.svg)

![Mac OS](https://img.shields.io/badge/mac%20os-FCC624?style=for-the-badge&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Alpine Linux](https://img.shields.io/badge/Alpine_Linux-0078D6.svg?style=for-the-badge&logo=alpine-linux&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Rasberry_Pi-FCC624.svg?style=for-the-badge&logo=raspberry-pi&logoColor=red)

This is a light version of [Pillow-Heif](https://github.com/bigcat88/pillow_heif) with more permissive license for binary wheels.

It includes only `HEIF` decoder and does not support `save` operations.

All codebase are the same, refer to [pillow-heif docs](https://pillow-heif.readthedocs.io/).

The distribution name is `pi-heif-decoder`; the Python import remains
`pi_heif`. Releases currently provide CPython 3.13 manylinux wheels for x86_64
and aarch64.

### License boundary

The wheel contains the BSD-licensed Python extension plus dynamically linked,
LGPL-licensed libheif and libde265. LGPL source and license locations are
recorded in `LICENSES_bundled.txt` inside the distribution.

### Install
```console
python3 -m pip install -U pip
python3 -m pip install pi-heif-decoder
```

### Example of use as a Pillow plugin
```python3
from PIL import Image
from pi_heif import register_heif_opener

register_heif_opener()

im = Image.open("images/input.heic")  # do whatever need with a Pillow image
im.show()
```

### 8/10/12 bit HEIF to 8/16 bit PNG using OpenCV
```python3
import numpy as np
import cv2
import pi_heif

heif_file = pi_heif.open_heif("image.heic", convert_hdr_to_8bit=False, bgr_mode=True)
np_array = np.asarray(heif_file)
cv2.imwrite("image.png", np_array)
```

### Get decoded image data as a Numpy array
```python3
import numpy as np
import pi_heif

if pi_heif.is_supported("input.heic"):
    heif_file = pi_heif.open_heif("input.heic")
    np_array = np.asarray(heif_file)
```

### Accessing Depth Images

```python3
from PIL import Image
from pillow_heif import register_heif_opener
import numpy as np

register_heif_opener()

im = Image.open("../tests/images/heif_other/pug.heic")
if im.info["depth_images"]:
    depth_im = im.info["depth_images"][0]  # Access the first depth image (usually there will be only one).
    # Depth images are instances of `class HeifDepthImage(BaseImage)`,
    # so work with them as you would with any usual image in pillow_heif.
    # Depending on what you need the depth image for, you can convert it to a NumPy array or convert it to a Pillow image.
    pil_im = depth_im.to_pillow()
    np_im = np.asarray(depth_im)
    print(pil_im)
    print(pil_im.info["metadata"])
```

### Wheels

| **_Wheels table_** | macOS<br/>Intel | macOS<br/>Silicon | Windows<br/> | musllinux* | manylinux* |
|--------------------|:---------------:|:-----------------:|:------------:|:----------:|:----------:|
| CPython 3.10       |        ✅        |         ✅         |      ✅       |     ✅      |     ✅      |
| CPython 3.11       |        ✅        |         ✅         |      ✅       |     ✅      |     ✅      |
| CPython 3.12       |        ✅        |         ✅         |      ✅       |     ✅      |     ✅      |
| CPython 3.13       |        ✅        |         ✅         |      ✅       |     ✅      |     ✅      |
| CPython 3.14       |        ✅        |         ✅         |      ✅       |     ✅      |     ✅      |
| CPython 3.14t      |        ✅        |         ✅         |      ✅       |     ✅      |     ✅      |
| PyPy 3.11 v7.3     |        ✅        |         ✅         |      ✅       |    N/A     |     ✅      |

&ast; **x86_64**, **aarch64** wheels.
