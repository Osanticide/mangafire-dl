import pytest

from mangafire.parser import (
    InvalidMangaFireURLError,
    parse_manga_id,
)


def test_parse_manga_id_from_id_only_url():
    assert parse_manga_id("https://mangafire.to/title/027") == "027"


def test_parse_manga_id_from_slug_url():
    assert parse_manga_id("https://mangafire.to/title/027-bleach") == "027"


def test_parse_manga_id_from_volume_url():
    assert parse_manga_id("https://mangafire.to/title/027/volume/616") == "027"


def test_parse_manga_id_from_chapter_url():
    assert parse_manga_id("https://mangafire.to/title/027/chapter/6056551") == "027"


def test_parse_manga_id_with_slug_and_volume():
    assert (
        parse_manga_id("https://mangafire.to/title/027-bleach/volume/144770") == "027"
    )


def test_parse_manga_id_rejects_wrong_domain():
    with pytest.raises(InvalidMangaFireURLError):
        parse_manga_id("https://example.com/title/027")


def test_parse_manga_id_rejects_wrong_path():
    with pytest.raises(InvalidMangaFireURLError):
        parse_manga_id("https://mangafire.to/manga/027")


def test_parse_manga_id_rejects_invalid_scheme():
    with pytest.raises(InvalidMangaFireURLError):
        parse_manga_id("ftp://mangafire.to/title/027")
