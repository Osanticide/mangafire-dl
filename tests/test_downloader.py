from unittest.mock import patch

import pytest

from mangafire.downloader import (
    GalleryDLDownloadError,
    GalleryDLDownloader,
)


def test_download_calls_gallery_dl_with_cbz():
    downloader = GalleryDLDownloader()

    with patch("mangafire.downloader.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0

        downloader.download("https://mangafire.to/title/027-bleach/volume/144857")

    mock_run.assert_called_once_with(
        [
            "gallery-dl",
            "--cbz",
            "https://mangafire.to/title/027-bleach/volume/144857",
        ],
        check=False,
    )


def test_download_accepts_successful_process():
    downloader = GalleryDLDownloader()

    with patch("mangafire.downloader.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0

        downloader.download("https://mangafire.to/title/027-bleach/volume/144857")


def test_download_raises_when_gallery_dl_fails():
    downloader = GalleryDLDownloader()

    with patch("mangafire.downloader.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1

        with pytest.raises(GalleryDLDownloadError) as exc_info:
            downloader.download("https://mangafire.to/title/027-bleach/volume/144857")

    assert exc_info.value.returncode == 1
    assert exc_info.value.url == "https://mangafire.to/title/027-bleach/volume/144857"
