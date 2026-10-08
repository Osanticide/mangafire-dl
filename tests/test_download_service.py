from unittest.mock import Mock

import pytest

from mangafire.download_service import MangaFireDownloadService
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
