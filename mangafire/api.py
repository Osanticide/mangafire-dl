from __future__ import annotations

from typing import Any

import requests

from .models import Volume
from .vrf import generate_vrf


class MangaFireAPI:
    """Cliente HTTP para a API do MangaFire."""

    BASE_URL = "https://mangafire.to"
    API_URL = f"{BASE_URL}/api"

    def __init__(self) -> None:
        self.session = requests.Session()

        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/152.0.0.0 "
                    "Safari/537.36 "
                    "OPR/136.0.0.0"
                ),
                "X-Requested-With": "XMLHttpRequest",
            }
        )

    def _get(self, endpoint: str) -> dict[str, Any]:
        """
        Faz uma requisição GET à API do MangaFire.

        O VRF é calculado antes da adição do parâmetro
        ?vrf= à requisição.
        """

        url = f"{self.API_URL}/{endpoint.lstrip('/')}"

        vrf = generate_vrf(url)

        response = self.session.get(
            url,
            params={"vrf": vrf},
            headers={
                "Referer": self.BASE_URL,
            },
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def get_volumes(self, manga_id: str) -> list[Volume]:
        """Obtém os volumes de um mangá."""

        data = self._get(f"titles/{manga_id}/volumes")

        return [
            Volume(
                id=item["id"],
                number=item["number"],
                name=item["name"],
                language=item["language"],
                chapter_count=item["chapterCount"],
            )
            for item in data["items"]
        ]
