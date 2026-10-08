from __future__ import annotations

from typing import Any

import requests

from .models import Chapter, Volume
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

    def _get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Faz uma requisição GET à API do MangaFire.

        O VRF é calculado sobre a URL antes da adição
        do parâmetro ?vrf=.
        """

        url = f"{self.API_URL}/{endpoint.lstrip('/')}"

        if params:
            from urllib.parse import urlencode

            query = urlencode(sorted(params.items()))
            url = f"{url}?{query}"

        vrf = generate_vrf(url)

        request_params = dict(params or {})
        request_params["vrf"] = vrf

        response = self.session.get(
            f"{self.API_URL}/{endpoint.lstrip('/')}",
            params=request_params,
            headers={
                "Referer": self.BASE_URL,
            },
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def _get_paginated(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Obtém todos os itens de um endpoint paginado."""

        all_items: list[dict[str, Any]] = []
        page = 1

        while True:
            page_params = dict(params or {})
            page_params.update(
                {
                    "page": page,
                    "limit": limit,
                }
            )

            data = self._get(endpoint, page_params)

            print(
                f"DEBUG: page={page} "
                f"items={len(data.get('items', []))} "
                f"meta={data.get('meta')}"
            )

            items = data.get("items", [])
            all_items.extend(items)

            meta = data.get("meta", {})

            if not data.get("hasNext", False):
                break

            page += 1

        return all_items

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

    def get_chapters(
        self,
        manga_id: str,
        language: str | None = None,
    ) -> list[Chapter]:
        """Obtém todos os capítulos de um mangá."""

        params: dict[str, Any] = {
            "sort": "number",
            "order": "desc",
        }

        if language is not None:
            params["language"] = language

        items = self._get_paginated(
            f"titles/{manga_id}/chapters",
            params=params,
        )

        return [
            Chapter(
                id=item["id"],
                number=item["number"],
                name=item["name"],
                language=item["language"],
                type=item["type"],
            )
            for item in items
        ]
