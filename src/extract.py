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

from enum import Enum
from pathlib import Path
from typing import Optional

import cv2
from arcaea_offline_ocr.device.rois.definition import DeviceRoisAutoT1, DeviceRoisAutoT2
from arcaea_offline_ocr.device.rois.extractor import DeviceRoisExtractor
from rich.progress import track

from src.utils import CropBlackEdges


class ExtractOption(Enum):
    PURE = "pure"
    FAR = "far"
    LOST = "lost"
    SCORE = "score"
    MAX_RECALL = "max_recall"

    JACKET = "jacket"
    PARTNER_ICON = "partner_icon"

    RATING_CLASS = "rating_class"
    CLEAR_STATUS = "clear_status"


class Extractor:
    LABEL = "ExtractorBase"
    DEFAULT_EXTRACT_OPTIONS = [
        ExtractOption.PURE,
        ExtractOption.FAR,
        ExtractOption.LOST,
        ExtractOption.SCORE,
        ExtractOption.MAX_RECALL,
        ExtractOption.JACKET,
        ExtractOption.PARTNER_ICON,
    ]

    def __init__(
        self,
        image_files: list[Path],
        output_dir: Path,
        options: Optional[list[ExtractOption]] = None,
    ):
        self.image_files = image_files
        self.output_dir = output_dir

        if options is None:
            self.options = self.DEFAULT_EXTRACT_OPTIONS.copy()
        else:
            self.options = options.copy()

    @staticmethod
    def get_extractor(image_file: Path) -> DeviceRoisExtractor:
        raise NotImplementedError()

    def extract(self):
        for _file in track(self.image_files, description=f"Extracting {self.LABEL}"):
            file = _file.resolve()
            extractor = self.get_extractor(file)

            output_file_base = self.output_dir / file.name

            if ExtractOption.PURE in self.options:
                output_file = output_file_base.with_stem(f"{file.stem}_pure")
                cv2.imwrite(str(output_file), extractor.pure)

            if ExtractOption.FAR in self.options:
                output_file = output_file_base.with_stem(f"{file.stem}_far")
                cv2.imwrite(str(output_file), extractor.far)

            if ExtractOption.LOST in self.options:
                output_file = output_file_base.with_stem(f"{file.stem}_lost")
                cv2.imwrite(str(output_file), extractor.lost)

            if ExtractOption.SCORE in self.options:
                output_file = output_file_base.with_stem(f"{file.stem}_score")
                cv2.imwrite(str(output_file), extractor.score)

            if ExtractOption.MAX_RECALL in self.options:
                output_file = output_file_base.with_stem(f"{file.stem}_max_recall")
                cv2.imwrite(str(output_file), extractor.max_recall)

            if ExtractOption.JACKET in self.options:
                output_file = output_file_base.with_stem(f"{file.stem}_jacket")
                cv2.imwrite(str(output_file), extractor.jacket)

            if ExtractOption.PARTNER_ICON in self.options:
                output_file = output_file_base.with_stem(f"{file.stem}_partner_icon")
                cv2.imwrite(str(output_file), extractor.partner_icon)

            if ExtractOption.RATING_CLASS in self.options:
                output_file = output_file_base.with_stem(f"{file.stem}_rating_class")
                cv2.imwrite(str(output_file), extractor.rating_class)

            if ExtractOption.CLEAR_STATUS in self.options:
                output_file = output_file_base.with_stem(f"{file.stem}_clear_status")
                cv2.imwrite(str(output_file), extractor.clear_status)


class T1Extractor(Extractor):
    @staticmethod
    def get_extractor(image_file: Path) -> DeviceRoisExtractor:
        img_raw = cv2.imread(str(image_file.resolve()), cv2.IMREAD_COLOR)
        img = CropBlackEdges.crop(img_raw, convert_flag=cv2.COLOR_BGR2GRAY)
        h, w = img.shape[:2]
        rois = DeviceRoisAutoT1(w=w, h=h)
        return DeviceRoisExtractor(img, rois)


class T2Extractor(Extractor):
    @staticmethod
    def get_extractor(image_file: Path) -> DeviceRoisExtractor:
        img_raw = cv2.imread(str(image_file.resolve()), cv2.IMREAD_COLOR)
        img = CropBlackEdges.crop(img_raw, convert_flag=cv2.COLOR_BGR2GRAY)
        h, w = img.shape[:2]
        rois = DeviceRoisAutoT2(w=w, h=h)
        return DeviceRoisExtractor(img, rois)
