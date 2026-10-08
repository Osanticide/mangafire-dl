from unittest.mock import Mock

import pytest

from mangafire.download_service import (
    DownloadProgress,
    MangaFireDownloadService,
)
from mangafire.downloader import GalleryDLDownloadError
from mangafire.models import Chapter, Volume
from mangafire.requests import DownloadRequest


class FakeResolver:
    def resolve_request(self, request):
        return [
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
            Volume(
                id=103,
                number=3,
                name="Volume 3",
                language="pt-br",
                chapter_count=8,
            ),
        ]


class FakeChapterResolver:
    def resolve_request(self, request):
        return [
            Chapter(
                id=201,
                number=1,
                name="Chapter 1",
                language="pt-br",
                type="unofficial",
            ),
            Chapter(
                id=202,
                number=2,
                name="Chapter 2",
                language="pt-br",
                type="unofficial",
            ),
        ]


def test_downloads_resources_sequentially():
    resolver = FakeResolver()
    downloader = Mock()

    service = MangaFireDownloadService(
        resolver=resolver,
        downloader=downloader,
    )

    request = DownloadRequest(
        manga_url="https://mangafire.to/title/027-bleach",
        language="pt-br",
        mode="volumes",
        selections=((1, 3),),
    )

    service.download(request)

    assert downloader.download.call_count == 3

    assert [call.args[0] for call in downloader.download.call_args_list] == [
        "https://mangafire.to/title/027-bleach/volume/101",
        "https://mangafire.to/title/027-bleach/volume/102",
        "https://mangafire.to/title/027-bleach/volume/103",
    ]


def test_downloads_chapters_sequentially():
    resolver = FakeChapterResolver()
    downloader = Mock()

    service = MangaFireDownloadService(
        resolver=resolver,
        downloader=downloader,
    )

    request = DownloadRequest(
        manga_url="https://mangafire.to/title/027-bleach",
        language="pt-br",
        mode="chapters",
        selections=((1, 2),),
    )

    service.download(request)

    assert downloader.download.call_count == 2

    assert [call.args[0] for call in downloader.download.call_args_list] == [
        "https://mangafire.to/title/027-bleach/chapter/201",
        "https://mangafire.to/title/027-bleach/chapter/202",
    ]


def test_download_stops_when_downloader_fails():
    resolver = FakeResolver()
    downloader = Mock()

    downloader.download.side_effect = [
        None,
        GalleryDLDownloadError(
            url="https://mangafire.to/title/027-bleach/volume/102",
            returncode=1,
        ),
    ]

    service = MangaFireDownloadService(
        resolver=resolver,
        downloader=downloader,
    )

    request = DownloadRequest(
        manga_url="https://mangafire.to/title/027-bleach",
        language="pt-br",
        mode="volumes",
        selections=((1, 3),),
    )

    with pytest.raises(GalleryDLDownloadError):
        service.download(request)

    assert downloader.download.call_count == 2


def test_download_reports_progress():
    resolver = FakeResolver()
    downloader = Mock()
    progress_callback = Mock()

    service = MangaFireDownloadService(
        resolver=resolver,
        downloader=downloader,
    )

    request = DownloadRequest(
        manga_url="https://mangafire.to/title/027-bleach",
        language="pt-br",
        mode="volumes",
        selections=((1, 3),),
    )

    service.download(
        request,
        progress_callback=progress_callback,
    )

    assert progress_callback.call_count == 6

    progress = [call.args[0] for call in progress_callback.call_args_list]

    assert all(isinstance(item, DownloadProgress) for item in progress)

    assert [(item.index, item.total, item.completed) for item in progress] == [
        (1, 3, False),
        (1, 3, True),
        (2, 3, False),
        (2, 3, True),
        (3, 3, False),
        (3, 3, True),
    ]

    assert [item.resource.number for item in progress] == [
        1,
        1,
        2,
        2,
        3,
        3,
    ]
