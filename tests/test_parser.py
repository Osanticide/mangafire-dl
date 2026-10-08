import pytest

from mangafire.parser import InvalidMangaFireURLError, parse_manga_id


def test_parse_title_url():
    assert parse_manga_id("https://mangafire.to/title/027") == "027"


def test_parse_title_slug_url():
    assert parse_manga_id("https://mangafire.to/title/027-bleach") == "027"


def test_parse_volume_url():
    assert parse_manga_id("https://mangafire.to/title/027/volume/616") == "027"


def test_parse_chapter_url():
    assert parse_manga_id("https://mangafire.to/title/027/chapter/6056551") == "027"


def test_reject_wrong_domain():
    with pytest.raises(InvalidMangaFireURLError):
        parse_manga_id("https://google.com/title/027")


def test_reject_wrong_path():
    with pytest.raises(InvalidMangaFireURLError):
        parse_manga_id("https://mangafire.to/other/027")


def test_reject_invalid_scheme():
    with pytest.raises(InvalidMangaFireURLError):
        parse_manga_id("ftp://mangafire.to/title/027")
