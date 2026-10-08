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

    assert captured.out == "mangafire-dl 0.2.0\n"


def test_help(capsys):
    parser = main.build_parser()

    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["--help"])

    assert exc_info.value.code == 0

    captured = capsys.readouterr()

    assert "Baixa volumes e capítulos do MangaFire" in captured.out
    assert "--version" in captured.out
    assert "--volumes" in captured.out
    assert "--chapters" in captured.out
    assert "Exemplos:" in captured.out


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

    assert "Erro de seleção:" in captured.err


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

    assert "Erro de URL:" in captured.err


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

    assert "Nenhum recurso foi encontrado" in captured.err


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

    assert "Erro durante o download:" in captured.err
    assert "código de saída 1" in captured.err


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

    assert "Erro inesperado: erro inesperado" in captured.err
