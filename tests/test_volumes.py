from mangafire.api import MangaFireAPI
from mangafire.models import Volume


def test_get_bleach_volumes():
    api = MangaFireAPI()

    volumes = api.get_volumes("027")

    assert len(volumes) > 0
    assert all(isinstance(volume, Volume) for volume in volumes)


def test_find_bleach_volume_14_pt_br():
    api = MangaFireAPI()

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
