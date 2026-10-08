from pathlib import Path

from mangafire.models import Chapter, Volume
from mangafire.output import (
    build_output_path,
    format_resource_number,
    resolve_output_directory,
    sanitize_path_component,
)


def test_resolve_output_directory_defaults_to_downloads():
    result = resolve_output_directory(None)

    assert result == Path.home() / "Downloads"


def test_resolve_output_directory_expands_user_home():
    result = resolve_output_directory("~/Mangas")

    assert result == Path.home() / "Mangas"


def test_sanitize_path_component():
    assert sanitize_path_component("Bleach: TYBW?") == "Bleach TYBW"


def test_format_integer_volume_number():
    assert format_resource_number(1, 2) == "01"
    assert format_resource_number(73, 2) == "73"


def test_format_integer_chapter_number():
    assert format_resource_number(1, 3) == "001"
    assert format_resource_number(12, 3) == "012"
    assert format_resource_number(123, 3) == "123"


def test_format_decimal_number():
    assert format_resource_number(636.5, 3) == "636.5"


def test_build_volume_output_path():
    resource = Volume(
        id=144857,
        number=73,
        name="Volume 73",
        language="pt-br",
        chapter_count=20,
    )

    result = build_output_path(
        output_directory="D:/Mangas",
        manga_url="https://mangafire.to/title/027-bleach",
        resource=resource,
    )

    assert result == Path("D:/Mangas/Bleach/volumes/Bleach - Volume 73.cbz")


def test_build_chapter_output_path():
    resource = Chapter(
        id=123456,
        number=1,
        name="Chapter 1",
        language="pt-br",
        type="official",
    )

    result = build_output_path(
        output_directory="D:/Mangas",
        manga_url="https://mangafire.to/title/027-bleach",
        resource=resource,
    )

    assert result == Path("D:/Mangas/Bleach/chapters/Bleach - Chapter 001.cbz")
