from mangafire.models import Volume
from mangafire.resolver import (
    InvalidVolumeRangeError,
    MangaFireResolver,
)


class FakeMangaFireAPI:
    def get_volumes(self, manga_id: str) -> list[Volume]:
        return [
            Volume(
                id=100,
                number=1,
                name="Volume 1",
                language="pt-br",
                chapter_count=10,
            ),
            Volume(
                id=101,
                number=2,
                name="Volume 2",
                language="pt-br",
                chapter_count=9,
            ),
            Volume(
                id=102,
                number=3,
                name="Volume 3",
                language="pt-br",
                chapter_count=8,
            ),
            Volume(
                id=200,
                number=1,
                name="Volume 1",
                language="en",
                chapter_count=10,
            ),
        ]


def test_resolve_volumes_by_language():
    resolver = MangaFireResolver(FakeMangaFireAPI())

    volumes = resolver.resolve_volumes(
        manga_id="027",
        language="pt-br",
        start=1,
        end=3,
    )

    assert len(volumes) == 3
    assert all(volume.language == "pt-br" for volume in volumes)


def test_resolve_volumes_by_range():
    resolver = MangaFireResolver(FakeMangaFireAPI())

    volumes = resolver.resolve_volumes(
        manga_id="027",
        language="pt-br",
        start=2,
        end=3,
    )

    assert [volume.number for volume in volumes] == [2, 3]


def test_resolve_volumes_ignores_other_languages():
    resolver = MangaFireResolver(FakeMangaFireAPI())

    volumes = resolver.resolve_volumes(
        manga_id="027",
        language="pt-br",
        start=1,
        end=1,
    )

    assert len(volumes) == 1
    assert volumes[0].language == "pt-br"


def test_resolve_volumes_returns_sorted_results():
    resolver = MangaFireResolver(FakeMangaFireAPI())

    volumes = resolver.resolve_volumes(
        manga_id="027",
        language="pt-br",
        start=1,
        end=3,
    )

    assert [volume.number for volume in volumes] == [1, 2, 3]


def test_invalid_volume_range():
    resolver = MangaFireResolver(FakeMangaFireAPI())

    try:
        resolver.resolve_volumes(
            manga_id="027",
            language="pt-br",
            start=3,
            end=1,
        )
    except InvalidVolumeRangeError:
        pass
    else:
        raise AssertionError("Era esperado InvalidVolumeRangeError.")
