from unittest.mock import patch

from mangafire.api import MangaFireAPI
from mangafire.models import Volume


def make_volume_item(
    volume_id: int,
    number: int,
    language: str,
    chapter_count: int,
) -> dict:
    return {
        "id": volume_id,
        "number": number,
        "name": f"Volume {number}",
        "language": language,
        "chapterCount": chapter_count,
    }


def test_get_bleach_volumes():
    api = MangaFireAPI()

    items = [
        make_volume_item(144857, 73, "pt-br", 10),
        make_volume_item(144855, 72, "pt-br", 9),
    ]

    with patch.object(
        api,
        "_get",
        return_value={"items": items},
    ) as mock_get:
        volumes = api.get_volumes("027")

    assert len(volumes) == 2
    assert all(isinstance(volume, Volume) for volume in volumes)
    assert [volume.number for volume in volumes] == [73, 72]

    mock_get.assert_called_once_with("titles/027/volumes")


def test_find_bleach_volume_14_pt_br():
    api = MangaFireAPI()

    items = [
        make_volume_item(144770, 14, "pt-br", 8),
        make_volume_item(144771, 14, "en", 8),
        make_volume_item(144772, 15, "pt-br", 9),
    ]

    with patch.object(
        api,
        "_get",
        return_value={"items": items},
    ):
        volumes = api.get_volumes("027")

    volume_14 = next(
        volume
        for volume in volumes
        if volume.language == "pt-br" and volume.number == 14
    )

    assert volume_14.id == 144770
    assert volume_14.number == 14
    assert volume_14.language == "pt-br"
    assert volume_14.chapter_count == 8
