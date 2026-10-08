from mangafire.models import Chapter, Volume
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


def test_resolve_chapters_prefers_official_on_first_ambiguity():
    resolver = MangaFireResolver(FakeChapterAPI())

    chapters = resolver.resolve_chapters(
        manga_id="027",
        language="en",
        start=1,
        end=1,
    )

    assert len(chapters) == 1
    assert chapters[0].type == "official"


def test_resolve_chapters_keeps_previous_choice():
    resolver = MangaFireResolver(FakeChapterAPI())

    chapters = resolver.resolve_chapters(
        manga_id="027",
        language="en",
        start=1,
        end=2,
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
        start=1,
        end=4,
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
        start=1,
        end=4,
    )

    assert [chapter.number for chapter in chapters] == [
        1,
        2,
        3,
        4,
    ]


def test_invalid_chapter_range():
    resolver = MangaFireResolver(FakeChapterAPI())

    try:
        resolver.resolve_chapters(
            manga_id="027",
            language="en",
            start=3,
            end=1,
        )
    except InvalidChapterRangeError:
        pass
    else:
        raise AssertionError("Era esperado InvalidChapterRangeError.")
