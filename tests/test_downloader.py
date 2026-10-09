from pathlib import Path
from unittest.mock import patch

import pytest

from mangafire.downloader import (
    GalleryDLArchiveNameError,
    GalleryDLArchiveNotFoundError,
    GalleryDLDownloadError,
    GalleryDLDownloader,
)


URL = "https://mangafire.to/title/027-bleach/volume/144857"


@pytest.fixture
def gallery_dl_mocks():
    with (
        patch("mangafire.downloader.config.clear") as mock_clear,
        patch("mangafire.downloader.config.set") as mock_set,
        patch("mangafire.downloader.job.DownloadJob") as mock_job,
    ):
        mock_job.return_value.run.return_value = 0

        yield mock_clear, mock_set, mock_job


def assert_gallery_dl_configuration(mock_set):
    calls = mock_set.call_args_list

    assert len(calls) == 2

    base_directory = calls[0].args[2]

    assert calls[0].args[:2] == (
        ("extractor",),
        "base-directory",
    )

    assert Path(base_directory).name.startswith("mangafire-dl-")

    assert calls[1].args == (
        ("extractor",),
        "postprocessors",
        [{"name": "zip", "extension": "cbz"}],
    )


def test_download_uses_python_api_and_moves_cbz(
    tmp_path,
    gallery_dl_mocks,
):
    mock_clear, mock_set, mock_job = gallery_dl_mocks
    downloader = GalleryDLDownloader()
    destination = tmp_path / "Bleach - Volume 73.cbz"
    archive = Path("temporary/v73.cbz")

    with (
        patch(
            "mangafire.downloader.Path.rglob",
            return_value=[archive],
        ),
        patch("mangafire.downloader.shutil.move") as mock_move,
    ):
        result = downloader.download(URL, destination)

    assert result == destination
    assert destination.parent.exists()

    mock_clear.assert_called_once()
    mock_job.assert_called_once_with(URL)
    mock_job.return_value.run.assert_called_once_with()

    assert_gallery_dl_configuration(mock_set)
    mock_move.assert_called_once_with(str(archive), str(destination))


def test_download_raises_when_gallery_dl_returns_error(
    tmp_path,
    gallery_dl_mocks,
):
    _, _, mock_job = gallery_dl_mocks
    downloader = GalleryDLDownloader()
    mock_job.return_value.run.return_value = 1

    with pytest.raises(GalleryDLDownloadError) as exc_info:
        downloader.download(URL, tmp_path / "volume.cbz")

    assert exc_info.value.returncode == 1
    assert exc_info.value.url == URL


def test_download_raises_when_no_cbz_is_produced(
    tmp_path,
    gallery_dl_mocks,
):
    downloader = GalleryDLDownloader()

    with patch(
        "mangafire.downloader.Path.rglob",
        return_value=[],
    ):
        with pytest.raises(GalleryDLArchiveNotFoundError):
            downloader.download(URL, tmp_path / "volume.cbz")


def test_download_raises_when_multiple_cbz_archives_are_produced(
    tmp_path,
    gallery_dl_mocks,
):
    downloader = GalleryDLDownloader()

    archives = [
        Path("temporary/volume-1.cbz"),
        Path("temporary/volume-2.cbz"),
    ]

    with patch(
        "mangafire.downloader.Path.rglob",
        return_value=archives,
    ):
        with pytest.raises(GalleryDLArchiveNotFoundError):
            downloader.download(URL, tmp_path / "volume.cbz")


def test_download_to_directory_preserves_archive_name(
    tmp_path,
    gallery_dl_mocks,
):
    _, mock_set, mock_job = gallery_dl_mocks
    downloader = GalleryDLDownloader()
    destination_directory = tmp_path / "volumes"
    archive = Path("temporary/v73.cbz")

    with (
        patch(
            "mangafire.downloader.Path.rglob",
            return_value=[archive],
        ),
        patch("mangafire.downloader.shutil.move") as mock_move,
    ):
        result = downloader.download_to_directory(
            URL,
            destination_directory,
        )

    expected = destination_directory / "v73.cbz"

    assert result == expected
    assert destination_directory.exists()

    mock_job.assert_called_once_with(URL)
    assert_gallery_dl_configuration(mock_set)
    mock_move.assert_called_once_with(str(archive), str(expected))


def test_parse_volume_archive_number():
    assert (
        GalleryDLDownloader.parse_archive_number(
            "v73.cbz",
            "volume",
        )
        == 73.0
    )


def test_parse_decimal_chapter_archive_number():
    assert (
        GalleryDLDownloader.parse_archive_number(
            "c686.5_Special One-shot (New!).cbz",
            "chapter",
        )
        == 686.5
    )


def test_parse_archive_number_rejects_unrecognized_name():
    with pytest.raises(GalleryDLArchiveNameError):
        GalleryDLDownloader.parse_archive_number(
            "unexpected.cbz",
            "volume",
        )
