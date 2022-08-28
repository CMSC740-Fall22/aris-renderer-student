import os
from typing import Union

import numpy as np
from PIL import Image


def save_image(file: Union[str, os.PathLike], array: np.ndarray, tonemap: bool = True, clip: bool = True):
    """save an np.ndarray as an image file

    array: [H, W, 3], float32, values in [0, 1]
    """
    if tonemap:
        array = tonemap_image(array)
    if clip:
        array = np.clip(array, 0, 1)

    ext = os.path.splitext(file)[1].lower()
    kwargs = {}
    if ext == ".jpg":
        kwargs["quality"] = 95
    elif ext == ".png":
        kwargs["optimize"] = True

    img = Image.fromarray((array * 255).astype(np.uint8))
    img.save(file, **kwargs)


def tonemap_image(img: np.ndarray):
    """Adapted from Nori"""
    img = img.copy()
    small = img < 0.0031308
    img[small] *= 12.92
    img[~small] = 1.055 * np.power(img[~small], 1/2.4) - 0.055
    return img
