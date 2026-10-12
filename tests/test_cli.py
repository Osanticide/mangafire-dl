from pathlib import Path
from unittest.mock import Mock

import pytest

from mangafire.models import Volume

from mangafire import cli as main
from mangafire.download_service import NoResourcesFoundError
from mangafire.downloader import (
    GalleryDLDownloadError,
    GalleryDLNotFoundError,
)
from mangafire.parser import InvalidMangaFireURLError


def test_version(capsys):
    parser = main.build_parser()

    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["--version"])

    assert exc_info.value.code == 0

    captured = capsys.readouterr()

    assert captured.out == "mangafire-dl 0.5.0\n"


def test_help(capsys):
    parser = main.build_parser()

    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["--help"])

    assert exc_info.value.code == 0

    captured = capsys.readouterr()

    assert "Download manga volumes and chapters from MangaFire" in captured.out
    assert "--version" in captured.out
    assert "--volumes" in captured.out
    assert "--chapters" in captured.out
    assert "--output" in captured.out
    assert "Examples:" in captured.out


def test_main_downloads_successfully(monkeypatch):
    service = Mock()

    monkeypatch.setattr(
        main,
        "MangaFireDownloadService",
        lambda: service,
    )

    monkeypatch.setattr(
        main.sys,
        "argv",
        [
            "mangafire-dl",
            "https://mangafire.to/title/027-bleach",
            "--lang",
            "pt-br",
            "--volumes",
            "72-73",
        ],
    )

    result = main.main()

    assert result == 0
    service.download.assert_called_once()

    assert service.download.call_args.kwargs["output_directory"] is None


def test_main_accepts_output_directory(monkeypatch):
    service = Mock()

    monkeypatch.setattr(
        main,
        "MangaFireDownloadService",
        lambda: service,
    )

    monkeypatch.setattr(
        main.sys,
        "argv",
        [
            "mangafire-dl",
            "https://mangafire.to/title/027-bleach",
            "--lang",
            "pt-br",
            "--volumes",
            "73",
            "--output",
            "D:/Mangas",
        ],
    )

    result = main.main()

    assert result == 0

    assert service.download.call_args.kwargs["output_directory"] == Path("D:/Mangas")


def test_main_handles_invalid_selection(monkeypatch, capsys):
    monkeypatch.setattr(
        main.sys,
        "argv",
        [
            "mangafire-dl",
            "https://mangafire.to/title/027-bleach",
            "--lang",
            "pt-br",
            "--volumes",
            "10-1",
        ],
    )

    result = main.main()

    assert result == 1

    captured = capsys.readouterr()

    assert "Selection error:" in captured.err
    assert "Invalid selection: 10-1" in captured.err


def test_main_handles_invalid_url(monkeypatch, capsys):
    service = Mock()

    service.download.side_effect = InvalidMangaFireURLError(
        "A URL não pertence ao MangaFire."
    )

    monkeypatch.setattr(
        main,
        "MangaFireDownloadService",
        lambda: service,
    )

    monkeypatch.setattr(
        main.sys,
        "argv",
        [
            "mangafire-dl",
            "https://example.com/title/027",
            "--lang",
            "pt-br",
            "--volumes",
            "1",
        ],
    )

    result = main.main()

    assert result == 1

    captured = capsys.readouterr()

    assert "URL error:" in captured.err
    assert "The provided URL is not a valid MangaFire URL." in captured.err


def test_main_handles_no_resources(monkeypatch, capsys):
    service = Mock()

    service.download.side_effect = NoResourcesFoundError(
        mode="volumes",
        language="pt-br",
        selections=((999, 999),),
    )

    monkeypatch.setattr(
        main,
        "MangaFireDownloadService",
        lambda: service,
    )

    monkeypatch.setattr(
        main.sys,
        "argv",
        [
            "mangafire-dl",
            "https://mangafire.to/title/027-bleach",
            "--lang",
            "pt-br",
            "--volumes",
            "999",
        ],
    )

    result = main.main()

    assert result == 1

    captured = capsys.readouterr()

    assert "Error:" in captured.err
    assert "No resources were found for the requested selection." in captured.err


def test_main_handles_gallery_dl_not_found(monkeypatch, capsys):
    service = Mock()

    service.download.side_effect = GalleryDLNotFoundError(
        executable="gallery-dl",
    )

    monkeypatch.setattr(
        main,
        "MangaFireDownloadService",
        lambda: service,
    )

    monkeypatch.setattr(
        main.sys,
        "argv",
        [
            "mangafire-dl",
            "https://mangafire.to/title/027-bleach",
            "--lang",
            "pt-br",
            "--volumes",
            "1",
        ],
    )

    result = main.main()

    assert result == 1

    captured = capsys.readouterr()

    assert "gallery-dl" in captured.err
    assert "PATH" in captured.err


def test_main_handles_gallery_dl_download_error(monkeypatch, capsys):
    service = Mock()

    service.download.side_effect = GalleryDLDownloadError(
        url="https://mangafire.to/title/027-bleach/volume/144857",
        returncode=1,
    )

    monkeypatch.setattr(
        main,
        "MangaFireDownloadService",
        lambda: service,
    )

    monkeypatch.setattr(
        main.sys,
        "argv",
        [
            "mangafire-dl",
            "https://mangafire.to/title/027-bleach",
            "--lang",
            "pt-br",
            "--volumes",
            "73",
        ],
    )

    result = main.main()

    assert result == 1

    captured = capsys.readouterr()

    assert "Download error:" in captured.err
    assert "gallery-dl exited with code 1" in captured.err


def test_main_handles_unexpected_error(monkeypatch, capsys):
    service = Mock()

    service.download.side_effect = RuntimeError("erro inesperado")

    monkeypatch.setattr(
        main,
        "MangaFireDownloadService",
        lambda: service,
    )

    monkeypatch.setattr(
        main.sys,
        "argv",
        [
            "mangafire-dl",
            "https://mangafire.to/title/027-bleach",
            "--lang",
            "pt-br",
            "--volumes",
            "1",
        ],
    )

    result = main.main()

    assert result == 1

    captured = capsys.readouterr()

    assert "Unexpected error:" in captured.err
    assert "An unexpected error occurred." in captured.err


def test_main_accepts_manga_id(monkeypatch):
    service = Mock()

    monkeypatch.setattr(
        main,
        "MangaFireDownloadService",
        lambda: service,
    )

    monkeypatch.setattr(
        main.sys,
        "argv",
        [
            "mangafire-dl",
            "v92q7",
            "--lang",
            "pt-br",
            "--volumes",
            "1",
        ],
    )

    result = main.main()

    assert result == 0
    service.download.assert_called_once()

    request = service.download.call_args.args[0]

    assert request.manga_url == "https://mangafire.to/title/v92q7"
    assert request.language == "pt-br"
    assert request.mode == "volumes"
    assert request.selections == ((1, 1),)


def test_main_accepts_list_chapters_arguments(monkeypatch):
    monkeypatch.setattr(
        main.sys,
        "argv",
        [
            "mangafire-dl",
            "v92q7",
            "--list",
            "chapters",
            "--lang",
            "pt-br",
        ],
    )

    parser = main.build_parser()
    args = parser.parse_args()

    assert args.url == "v92q7"
    assert args.list == "chapters"
    assert args.lang == "pt-br"


def test_main_accepts_list_volumes_arguments(monkeypatch):
    monkeypatch.setattr(
        main.sys,
        "argv",
        [
            "mangafire-dl",
            "v92q7",
            "--list",
            "volumes",
            "--lang",
            "pt-br",
        ],
    )

    parser = main.build_parser()
    args = parser.parse_args()

    assert args.url == "v92q7"
    assert args.list == "volumes"
    assert args.lang == "pt-br"


import pytest


@pytest.mark.parametrize(
    "list_type, download_option, selection",
    [
        ("chapters", "--chapters", "1-10"),
        ("volumes", "--volumes", "1-5"),
        ("chapters", "--volumes", "1-5"),
        ("volumes", "--chapters", "1-10"),
    ],
)
def test_list_cannot_be_combined_with_download_selection(
    monkeypatch,
    list_type,
    download_option,
    selection,
):
    monkeypatch.setattr(
        main.sys,
        "argv",
        [
            "mangafire-dl",
            "v92q7",
            "--list",
            list_type,
            "--lang",
            "pt-br",
            download_option,
            selection,
        ],
    )

    parser = main.build_parser()

    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args()

    assert exc_info.value.code == 2


@pytest.mark.parametrize("list_type", ["chapters", "volumes"])
def test_list_requires_language(monkeypatch, list_type):
    monkeypatch.setattr(
        main.sys,
        "argv",
        [
            "mangafire-dl",
            "v92q7",
            "--list",
            list_type,
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        main.main()

    assert exc_info.value.code == 2


@pytest.mark.parametrize(
    "list_type",
    ["chapters", "volumes"],
)
def test_list_with_language_does_not_require_download_selection(
    monkeypatch,
    list_type,
):
    monkeypatch.setattr(
        main.sys,
        "argv",
        [
            "mangafire-dl",
            "v92q7",
            "--list",
            list_type,
            "--lang",
            "pt-br",
        ],
    )

    parser = main.build_parser()
    args = parser.parse_args()

    assert args.list == list_type
    assert args.lang == "pt-br"
    assert args.chapters is None
    assert args.volumes is None


def test_main_lists_volumes(monkeypatch, capsys):
    service = Mock()
    service.list_volumes.return_value = [
        Volume(
            id=101,
            number=1,
            name="Volume 1",
            language="pt-br",
            chapter_count=10,
        ),
        Volume(
            id=102,
            number=2,
            name="Volume 2",
            language="pt-br",
            chapter_count=9,
        ),
    ]

    monkeypatch.setattr(
        main,
        "MangaFireDownloadService",
        lambda: service,
    )
    monkeypatch.setattr(
        main.sys,
        "argv",
        [
            "mangafire-dl",
            "v92q7",
            "--list",
            "volumes",
            "--lang",
            "pt-br",
        ],
    )

    result = main.main()

    assert result == 0
    service.list_volumes.assert_called_once_with(
        manga_url="https://mangafire.to/title/v92q7",
        language="pt-br",
    )
    service.download.assert_not_called()
    service.download_direct.assert_not_called()
