from unittest.mock import patch

from mangafire.api import MangaFireAPI
from mangafire.models import Manga


def test_get_manga():
    api = MangaFireAPI()

    response = {
        "data": {
            "id": 46757,
            "hid": "v92q7",
            "slug": "kagurabachii",
            "title": "Kagurabachi",
            "type": "manga",
        }
    }

    with patch.object(
        api,
        "_get",
        return_value=response,
    ) as mock_get:
        manga = api.get_manga("v92q7")

    assert isinstance(manga, Manga)
    assert manga.id == "v92q7"
    assert manga.title == "Kagurabachi"

    mock_get.assert_called_once_with("titles/v92q7")
