from unittest.mock import patch

from mangafire.api import MangaFireAPI
from mangafire.models import Chapter


def make_chapter_item(number: int, language: str) -> dict:
    return {
        "id": 1000 + number,
        "number": str(number),
        "name": f"Chapter {number}",
        "language": language,
        "type": "official",
    }


def test_get_bleach_chapters_pt_br():
    api = MangaFireAPI()

    items = [
        make_chapter_item(1, "pt-br"),
        make_chapter_item(2, "pt-br"),
    ]

    with patch.object(
        api,
        "_get_paginated",
        return_value=items,
    ) as mock_paginated:
        chapters = api.get_chapters(
            "027",
            language="pt-br",
        )

    assert len(chapters) == 2
    assert all(isinstance(chapter, Chapter) for chapter in chapters)
    assert all(chapter.language == "pt-br" for chapter in chapters)

    mock_paginated.assert_called_once_with(
        "titles/027/chapters",
        params={
            "sort": "number",
            "order": "desc",
            "language": "pt-br",
        },
    )


def test_bleach_chapters_are_paginated():
    api = MangaFireAPI()

    pages = [
        {
            "items": [make_chapter_item(number, "en") for number in range(1, 21)],
            "meta": {"hasNext": True},
        },
        {
            "items": [make_chapter_item(number, "en") for number in range(21, 41)],
            "meta": {"hasNext": True},
        },
        {
            "items": [make_chapter_item(number, "en") for number in range(41, 46)],
            "meta": {"hasNext": False},
        },
    ]

    with patch.object(
        api,
        "_get",
        side_effect=pages,
    ) as mock_get:
        chapters = api.get_chapters(
            "027",
            language="en",
        )

    assert len(chapters) == 45
    assert all(isinstance(chapter, Chapter) for chapter in chapters)
    assert all(chapter.language == "en" for chapter in chapters)

    assert mock_get.call_count == 3

    calls = mock_get.call_args_list
    assert [call.args[1]["page"] for call in calls] == [1, 2, 3]
    assert all(call.args[1]["limit"] == 20 for call in calls)
    assert all(call.args[1]["language"] == "en" for call in calls)
