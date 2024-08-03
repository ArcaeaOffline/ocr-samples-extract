"""
Copyright (C) 2024 He Lin <log_283375@163.com>

This file is part of Arcaea Offline OCR samples extract.

Arcaea Offline OCR samples extract is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Arcaea Offline OCR samples extract is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Arcaea Offline OCR samples extract. If not, see <https://www.gnu.org/licenses/>.
"""

import math

import cv2
import numpy as np


def crop_xywh(mat: np.ndarray, rect: tuple[int, int, int, int]):
    x, y, w, h = rect
    return mat[y : y + h, x : x + w]


class CropBlackEdges:
    @staticmethod
    def is_black_edge(__img_gray_slice, black_pixel: int, ratio: float = 0.6):
        pixels_compared = __img_gray_slice < black_pixel
        return np.count_nonzero(pixels_compared) > math.floor(
            __img_gray_slice.size * ratio
        )

    @classmethod
    def get_crop_rect(cls, img_gray, black_threshold: int = 25):
        height, width = img_gray.shape[:2]
        left = 0
        right = width
        top = 0
        bottom = height

        for i in range(width):
            column = img_gray[:, i]
            if not cls.is_black_edge(column, black_threshold):
                break
            left += 1

        for i in sorted(range(width), reverse=True):
            column = img_gray[:, i]
            if i <= left + 1 or not cls.is_black_edge(column, black_threshold):
                break
            right -= 1

        assert right > left, "cropped width < 0"
        assert bottom > top, "cropped height < 0"
        return (left, top, right - left, bottom - top)

    @classmethod
    def crop(cls, img, convert_flag: cv2.COLOR_BGR2GRAY, black_threshold: int = 25):
        rect = cls.get_crop_rect(cv2.cvtColor(img, convert_flag), black_threshold)
        return crop_xywh(img, rect)
