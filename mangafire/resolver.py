from __future__ import annotations

from .api import MangaFireAPI
from .models import Volume


class InvalidVolumeRangeError(ValueError):
    """Indica que o intervalo de volumes é inválido."""


class MangaFireResolver:
    """Resolve recursos do MangaFire a partir dos critérios do usuário."""

    def __init__(self, api: MangaFireAPI | None = None) -> None:
        self.api = api or MangaFireAPI()

    def resolve_volumes(
        self,
        manga_id: str,
        language: str,
        start: float,
        end: float,
    ) -> list[Volume]:
        """Resolve os volumes de um mangá dentro de um intervalo e idioma."""

        if start > end:
            raise InvalidVolumeRangeError(
                "O volume inicial não pode ser maior que o volume final."
            )

        volumes = self.api.get_volumes(manga_id)

        matching_volumes = [
            volume
            for volume in volumes
            if volume.language == language and start <= volume.number <= end
        ]

        return sorted(
            matching_volumes,
            key=lambda volume: volume.number,
        )
