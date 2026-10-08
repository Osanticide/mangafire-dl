from pathlib import Path
from unittest.mock import patch

import pytest

from mangafire.downloader import (
    GalleryDLArchiveNotFoundError,
    GalleryDLDownloadError,
    GalleryDLDownloader,
)


def test_download_calls_gallery_dl_with_cbz_and_destination(
    tmp_path,
):
    downloader = GalleryDLDownloader()
    destination = tmp_path / "Bleach - Volume 73.cbz"

    with patch("mangafire.downloader.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0

        with patch(
            "mangafire.downloader.Path.rglob",
            return_value=[
                Path("temporary/volume.cbz"),
            ],
        ):
            with patch("mangafire.downloader.shutil.move") as mock_move:
                downloader.download(
                    "https://mangafire.to/title/027-bleach/volume/144857",
                    destination,
                )

    args = mock_run.call_args.args[0]

    assert args[0] == "gallery-dl"
    assert args[1] == "--config-ignore"
    assert args[2] == "--cbz"
    assert args[3] == "-d"
    assert args[5] == ("https://mangafire.to/title/027-bleach/volume/144857")

    mock_run.assert_called_once()
    mock_move.assert_called_once()


def test_download_accepts_successful_process(
    tmp_path,
):
    downloader = GalleryDLDownloader()
    destination = tmp_path / "Bleach - Volume 73.cbz"

    with patch("mangafire.downloader.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0

        with patch(
            "mangafire.downloader.Path.rglob",
            return_value=[
                Path("temporary/volume.cbz"),
            ],
        ):
            with patch("mangafire.downloader.shutil.move"):
                result = downloader.download(
                    "https://mangafire.to/title/027-bleach/volume/144857",
                    destination,
                )

    assert result == destination


def test_download_raises_when_gallery_dl_fails(
    tmp_path,
):
    downloader = GalleryDLDownloader()
    destination = tmp_path / "Bleach - Volume 73.cbz"

    with patch("mangafire.downloader.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1

        with pytest.raises(GalleryDLDownloadError) as exc_info:
            downloader.download(
                "https://mangafire.to/title/027-bleach/volume/144857",
                destination,
            )

    assert exc_info.value.returncode == 1
    assert exc_info.value.url == ("https://mangafire.to/title/027-bleach/volume/144857")


def test_download_raises_when_no_cbz_is_produced(
    tmp_path,
):
    downloader = GalleryDLDownloader()
    destination = tmp_path / "Bleach - Volume 73.cbz"

    with patch("mangafire.downloader.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0

        with patch(
            "mangafire.downloader.Path.rglob",
            return_value=[],
        ):
            with pytest.raises(GalleryDLArchiveNotFoundError):
                downloader.download(
                    "https://mangafire.to/title/027-bleach/volume/144857",
                    destination,
                )
