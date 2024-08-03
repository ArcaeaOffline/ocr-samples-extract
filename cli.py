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

import questionary
from rich.console import Console
from rich.table import Table

from src.extract import ExtractOption, Extractor, T1Extractor, T2Extractor

console = Console()

DEFAULT_SOURCES_PATH = Path("sources").resolve()
DEFAULT_OUTPUT_PATH = Path("outputs").resolve()


class SourcesType(Enum):
    T1 = "T1"
    T2 = "T2"


class PathExistValidator(questionary.Validator):
    def validate(self, document):
        path = Path(document.text)

        if not path.exists():
            raise questionary.ValidationError(
                message="Please choose a valid path.",
                cursor_position=len(document.text),
            )


def ask_sources_path() -> Optional[Path]:
    sources_path = questionary.path(
        "Path of the source images directory?",
        default=str(DEFAULT_SOURCES_PATH) if DEFAULT_SOURCES_PATH.exists() else "",
        validate=PathExistValidator,
    ).ask()

    if sources_path is None:
        return None

    return Path(sources_path)


def ask_sources_type() -> Optional[SourcesType]:
    sources_type = questionary.select(
        "Which type is it?",
        choices=["T1", "T2"],
    ).ask()

    if sources_type is None:
        return None

    return SourcesType[sources_type]


def ask_output_path() -> Optional[Path]:
    output_path = questionary.path(
        "Path of the output directory?",
        default=str(DEFAULT_OUTPUT_PATH) if DEFAULT_OUTPUT_PATH.exists() else "",
    ).ask()

    if output_path is None:
        return None

    output_path = Path(output_path)

    if not output_path.exists():
        confirm_create = questionary.confirm(
            f"Output directory [{output_path.name}] does not exist. Create it?",
            qmark="!> ",
        ).ask()

        if not confirm_create:
            return None

        output_path.mkdir(parents=True)

    return output_path


def ask_extract_options() -> Optional[list[ExtractOption]]:
    def option_to_choice(option: ExtractOption) -> questionary.Choice:
        return questionary.Choice(
            title=option.value,
            value=option,
            checked=option in Extractor.DEFAULT_EXTRACT_OPTIONS,
        )

    choices = questionary.checkbox(
        "Extract what components?",
        [option_to_choice(option) for option in ExtractOption._member_map_.values()],
    ).ask()
    return choices


def abort():
    questionary.print("Abort.", style="yellow")
    raise SystemExit(1)


def extract(
    *,
    sources_path: Path,
    output_path: Path,
    sources_type: SourcesType,
    extract_options: list[ExtractOption],
):
    globs = ["*.jpg", "*.png", "*.jpeg"]

    table = Table(title="Summary", show_header=False)

    table.add_column("Key", justify="right", style="blue", no_wrap=True)
    table.add_column("Value")

    table.add_row("From", str(sources_path.resolve()))
    table.add_row("To", str(output_path.resolve()))
    table.add_row("Type", sources_type.value)
    table.add_row("Options", ", ".join([option.value for option in extract_options]))
    table.add_row("Globs", ", ".join(globs))

    console.print(table)

    confirm = questionary.confirm("Is this OK?").ask()
    if not confirm:
        abort()

    image_files = []
    [image_files.extend(sources_path.rglob(g)) for g in globs]

    if sources_type == SourcesType.T1:
        extractor = T1Extractor(
            image_files=image_files, output_dir=output_path, options=extract_options
        )
    elif sources_type == SourcesType.T2:
        extractor = T2Extractor(
            image_files=image_files, output_dir=output_path, options=extract_options
        )
    else:
        raise ValueError(f"wait waht is {sources_type!r}")

    extractor.extract()


if __name__ == "__main__":
    sources_path = ask_sources_path() or abort()
    sources_type = ask_sources_type() or abort()
    output_path = ask_output_path() or abort()
    extract_options = ask_extract_options() or abort()

    extract(
        sources_path=sources_path,
        output_path=output_path,
        sources_type=sources_type,
        extract_options=extract_options,
    )
