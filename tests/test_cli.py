from pathlib import Path
from unittest.mock import Mock

import pytest

import main
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

    assert captured.out == "mangafire-dl 0.4.0\n"


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
