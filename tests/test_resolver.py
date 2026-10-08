from mangafire.models import Chapter, Volume
from mangafire.requests import DownloadRequest
from mangafire.resolver import (
    InvalidChapterRangeError,
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
                id=103,
                number=4,
                name="Volume 4",
                language="pt-br",
                chapter_count=8,
            ),
            Volume(
                id=104,
                number=5,
                name="Volume 5",
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


class FakeChapterAPI:
    def get_chapters(
        self,
        manga_id: str,
        language: str | None = None,
    ) -> list[Chapter]:
        return [
            Chapter(
                id=1,
                number=1,
                name="Chapter 1",
                language="en",
                type="official",
            ),
            Chapter(
                id=2,
                number=1,
                name="Chapter 1",
                language="en",
                type="unofficial",
            ),
            Chapter(
                id=3,
                number=2,
                name="Chapter 2",
                language="en",
                type="official",
            ),
            Chapter(
                id=4,
                number=2,
                name="Chapter 2",
                language="en",
                type="unofficial",
            ),
            Chapter(
                id=5,
                number=3,
                name="Chapter 3",
                language="en",
                type="unofficial",
            ),
            Chapter(
                id=6,
                number=4,
                name="Chapter 4",
                language="en",
                type="official",
            ),
            Chapter(
                id=7,
                number=4,
                name="Chapter 4",
                language="en",
                type="unofficial",
            ),
            Chapter(
                id=8,
                number=5,
                name="Chapter 5",
                language="en",
                type="unofficial",
            ),
            Chapter(
                id=9,
                number=6,
                name="Chapter 6",
                language="en",
                type="unofficial",
            ),
            Chapter(
                id=10,
                number=12,
                name="Chapter 12",
                language="en",
                type="unofficial",
            ),
            Chapter(
                id=11,
                number=636.5,
                name="Special Chapter",
                language="en",
                type="unofficial",
            ),
        ]


def test_resolve_volumes_by_language():
    resolver = MangaFireResolver(FakeMangaFireAPI())

    volumes = resolver.resolve_volumes(
        manga_id="027",
        language="pt-br",
        selections=((1, 3),),
    )

    assert len(volumes) == 3
    assert all(volume.language == "pt-br" for volume in volumes)


def test_resolve_volumes_by_range():
    resolver = MangaFireResolver(FakeMangaFireAPI())

    volumes = resolver.resolve_volumes(
        manga_id="027",
        language="pt-br",
        selections=((2, 3),),
    )

    assert [volume.number for volume in volumes] == [2, 3]


def test_resolve_volumes_by_individual_selections():
    resolver = MangaFireResolver(FakeMangaFireAPI())

    volumes = resolver.resolve_volumes(
        manga_id="027",
        language="pt-br",
        selections=(
            (1, 1),
            (3, 3),
            (5, 5),
        ),
    )

    assert [volume.number for volume in volumes] == [1, 3, 5]


def test_resolve_volumes_with_mixed_selections():
    resolver = MangaFireResolver(FakeMangaFireAPI())

    volumes = resolver.resolve_volumes(
        manga_id="027",
        language="pt-br",
        selections=(
            (1, 2),
            (5, 5),
        ),
    )

    assert [volume.number for volume in volumes] == [1, 2, 5]


def test_resolve_volumes_ignores_other_languages():
    resolver = MangaFireResolver(FakeMangaFireAPI())

    volumes = resolver.resolve_volumes(
        manga_id="027",
        language="pt-br",
        selections=((1, 1),),
    )

    assert len(volumes) == 1
    assert volumes[0].language == "pt-br"


def test_resolve_volumes_returns_sorted_results():
    resolver = MangaFireResolver(FakeMangaFireAPI())

    volumes = resolver.resolve_volumes(
        manga_id="027",
        language="pt-br",
        selections=(
            (3, 3),
            (1, 1),
            (2, 2),
        ),
    )

    assert [volume.number for volume in volumes] == [1, 2, 3]


def test_invalid_volume_selection():
    resolver = MangaFireResolver(FakeMangaFireAPI())

    try:
        resolver.resolve_volumes(
            manga_id="027",
            language="pt-br",
            selections=(),
        )
    except InvalidVolumeRangeError:
        pass
    else:
        raise AssertionError("Era esperado InvalidVolumeRangeError.")


def test_resolve_chapters_prefers_official_on_first_ambiguity():
    resolver = MangaFireResolver(FakeChapterAPI())

    chapters = resolver.resolve_chapters(
        manga_id="027",
        language="en",
        selections=((1, 1),),
    )

    assert len(chapters) == 1
    assert chapters[0].type == "official"


def test_resolve_chapters_keeps_previous_choice():
    resolver = MangaFireResolver(FakeChapterAPI())

    chapters = resolver.resolve_chapters(
        manga_id="027",
        language="en",
        selections=((1, 2),),
    )

    assert [chapter.type for chapter in chapters] == [
        "official",
        "official",
    ]


def test_resolve_chapters_single_version_changes_preference():
    resolver = MangaFireResolver(FakeChapterAPI())

    chapters = resolver.resolve_chapters(
        manga_id="027",
        language="en",
        selections=((1, 4),),
    )

    assert [chapter.type for chapter in chapters] == [
        "official",
        "official",
        "unofficial",
        "unofficial",
    ]


def test_resolve_chapters_returns_one_chapter_per_number():
    resolver = MangaFireResolver(FakeChapterAPI())

    chapters = resolver.resolve_chapters(
        manga_id="027",
        language="en",
        selections=((1, 4),),
    )

    assert [chapter.number for chapter in chapters] == [
        1,
        2,
        3,
        4,
    ]


def test_resolve_chapters_individual_selections():
    resolver = MangaFireResolver(FakeChapterAPI())

    chapters = resolver.resolve_chapters(
        manga_id="027",
        language="en",
        selections=(
            (1, 1),
            (3, 3),
            (6, 6),
            (12, 12),
        ),
    )

    assert [chapter.number for chapter in chapters] == [
        1,
        3,
        6,
        12,
    ]


def test_resolve_chapters_mixed_selections():
    resolver = MangaFireResolver(FakeChapterAPI())

    chapters = resolver.resolve_chapters(
        manga_id="027",
        language="en",
        selections=(
            (1, 2),
            (5, 6),
            (12, 12),
        ),
    )

    assert [chapter.number for chapter in chapters] == [
        1,
        2,
        5,
        6,
        12,
    ]


def test_resolve_chapters_special_decimal():
    resolver = MangaFireResolver(FakeChapterAPI())

    chapters = resolver.resolve_chapters(
        manga_id="027",
        language="en",
        selections=((636.5, 636.5),),
    )

    assert len(chapters) == 1
    assert chapters[0].number == 636.5


def test_invalid_chapter_selection():
    resolver = MangaFireResolver(FakeChapterAPI())

    try:
        resolver.resolve_chapters(
            manga_id="027",
            language="en",
            selections=(),
        )
    except InvalidChapterRangeError:
        pass
    else:
        raise AssertionError("Era esperado InvalidChapterRangeError.")


def test_resolve_request_volumes():
    resolver = MangaFireResolver(FakeMangaFireAPI())

    request = DownloadRequest(
        manga_url="https://mangafire.to/title/027",
        language="pt-br",
        mode="volumes",
        selections=(
            (1, 2),
            (5, 5),
        ),
    )

    result = resolver.resolve_request(request)

    assert [volume.number for volume in result] == [1, 2, 5]


def test_resolve_request_chapters():
    resolver = MangaFireResolver(FakeChapterAPI())

    request = DownloadRequest(
        manga_url="https://mangafire.to/title/027-bleach",
        language="en",
        mode="chapters",
        selections=(
            (1, 2),
            (636.5, 636.5),
        ),
    )

    result = resolver.resolve_request(request)

    assert [chapter.number for chapter in result] == [
        1,
        2,
        636.5,
    ]
