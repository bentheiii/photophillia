from __future__ import annotations

from dataclasses import dataclass, asdict
from functools import lru_cache
from os.path import exists
from typing import NamedTuple

from abc import ABC, abstractmethod

import cv2
import numpy as np
from cv2.cv2 import imread
from math import gcd


@lru_cache()
def ratio(a, b):
    d = gcd(a, b)
    return a // d, b // d


class Size(NamedTuple):
    width: int
    height: int

    def pixel_count(self):
        return self.width * self.height

    def expected_shape(self, pix_depth=3):
        if not pix_depth:
            return self.width, self.height
        return self.width, self.height, pix_depth

    def has_pixel(self, other: Pixel):
        return other.x < self.width and other.y < self.height

    def ratio(self):
        return ratio(self.width, self.height)

    def __truediv__(self, other: Size):
        return self.width / other.width, self.height / other.height

    def __mul__(self, other):
        return Size(self.width * other, self.height * other)

    def __sub__(self, other: Pixel):
        return Size(self.width - other.x, self.height - other.y)

    def min(self, other):
        return Size(
            min(self.width, other.width),
            min(self.height, other.width)
        )

    @classmethod
    def from_array(cls, arr):
        height, width, _ = arr
        return Size(width, height)


class Pixel(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Size) -> Pixel:
        return type(self)(self.x + other.width, self.y + other.height)


class Color(NamedTuple):
    r: int
    g: int
    b: int

    def cv(self):
        return self.b, self.g, self.r


class Rectangle(NamedTuple):
    top: int
    left: int
    width: int
    height: int

    def size(self):
        return Size(self.width, self.height)

    def top_left(self):
        return Pixel(self.left, self.top)

    def __eq__(self, other):
        if isinstance(other, Size):
            return self.top_left() == Pixel(0, 0) \
                   and self.size() == other
        return super().__eq__(other)

    def crop_arr(self, arr):
        return arr[
               self.top:self.top + self.height,
               self.left:self.left + self.width,
               ]


class Photo(ABC):
    @abstractmethod
    def is_available(self) -> bool:
        pass

    @abstractmethod
    def raw_size(self) -> Size:
        pass

    @abstractmethod
    def raw_bmp(self) -> np.ndarray:
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass


class FilePhoto(Photo):
    def __init__(self, path: str):
        self.path = path

        self._raw_bmp = None

    def is_available(self) -> bool:
        return exists(self.path)

    def raw_size(self) -> Size:
        if self._raw_bmp:
            return Size.from_array(self._raw_bmp)

        try:
            import imagesize
        except ImportError:
            imagesize = None
        else:
            return imagesize.get(self.path)

        return Size.from_array(self.raw_bmp(cache=False))

    def raw_bmp(self, cache=True) -> np.ndarray:
        if self._raw_bmp is None:
            ret = imread(self.path)
            if cache:
                self._raw_bmp = ret
            return ret
        return self._raw_bmp

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return other.path == self.path
        return super().__eq__(other)

    def __hash__(self):
        return hash((type(self), self.path))

    def __str__(self):
        return self.path


@dataclass
class PhotoPositioning:
    source: Photo
    dest_size: Size
    background_color: Color

    crop: Rectangle

    scale: float
    dest_pix: Pixel

    def to_dict(self):
        ret = asdict(self)
        del ret['source']

    def make(self) -> np.ndarray:
        ret = np.empty(self.dest_size, 'i1')
        ret[:, :] = self.background_color.cv()

        src = self.source.raw_bmp()
        src = self.crop.crop_arr(src)
        src = cv2.resize(src, None, fx=self.scale, fy=self.scale)

        source_window = (self.dest_size - self.dest_pix).min(Size.from_array(src))
        src = Rectangle(0, 0, *source_window).crop_arr(src)

        dest_rect = Rectangle(*self.dest_pix, *source_window)
        dest_rect.crop_arr(ret)[:] = src

        return ret
