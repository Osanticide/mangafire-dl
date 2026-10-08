from mangafire.models import Chapter, Volume
from mangafire.urls import build_chapter_url, build_volume_url


def test_build_volume_url():
    volume = Volume(
        id=616,
        number=74,
        name="The Death and the Strawberry",
        language="en",
        chapter_count=12,
    )

    assert (
        build_volume_url(
            "https://mangafire.to/title/027",
            volume,
        )
        == "https://mangafire.to/title/027/volume/616"
    )


def test_build_volume_url_with_trailing_slash():
    volume = Volume(
        id=616,
        number=74,
        name="The Death and the Strawberry",
        language="en",
        chapter_count=12,
    )

    assert (
        build_volume_url(
            "https://mangafire.to/title/027/",
            volume,
        )
        == "https://mangafire.to/title/027/volume/616"
    )


def test_build_chapter_url():
    chapter = Chapter(
        id=6056551,
        number=686.5,
        name="Special One-shot (New!)",
        language="en",
        type="unofficial",
    )

    assert (
        build_chapter_url(
            "https://mangafire.to/title/027",
            chapter,
        )
        == "https://mangafire.to/title/027/chapter/6056551"
    )


def test_build_chapter_url_with_slug():
    chapter = Chapter(
        id=6056551,
        number=686.5,
        name="Special One-shot (New!)",
        language="en",
        type="unofficial",
    )

    assert (
        build_chapter_url(
            "https://mangafire.to/title/027-bleach",
            chapter,
        )
        == "https://mangafire.to/title/027-bleach/chapter/6056551"
    )
