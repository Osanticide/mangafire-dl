from mangafire.api import MangaFireAPI
from mangafire.models import Chapter


def test_get_bleach_chapters_pt_br():
    api = MangaFireAPI()

    chapters = api.get_chapters(
        "027",
        language="pt-br",
    )

    assert len(chapters) > 0
    assert all(isinstance(chapter, Chapter) for chapter in chapters)
    assert all(chapter.language == "pt-br" for chapter in chapters)


def test_bleach_chapters_are_paginated():
    api = MangaFireAPI()

    chapters = api.get_chapters(
        "027",
        language="en",
    )

    assert len(chapters) > 20
