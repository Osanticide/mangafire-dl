from __future__ import annotations

from .api import MangaFireAPI
from .models import Chapter, Volume


class InvalidVolumeRangeError(ValueError):
    """Indica que o intervalo de volumes é inválido."""


class InvalidChapterRangeError(ValueError):
    """Indica que o intervalo de capítulos é inválido."""


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

    def resolve_chapters(
        self,
        manga_id: str,
        language: str,
        start: float,
        end: float,
    ) -> list[Chapter]:
        """Resolve os capítulos de um mangá dentro de um intervalo e idioma."""

        if start > end:
            raise InvalidChapterRangeError(
                "O capítulo inicial não pode ser maior que o capítulo final."
            )

        chapters = self.api.get_chapters(
            manga_id,
            language=language,
        )

        matching_chapters = [
            chapter for chapter in chapters if start <= chapter.number <= end
        ]

        chapters_by_number: dict[float, list[Chapter]] = {}

        for chapter in matching_chapters:
            chapters_by_number.setdefault(
                chapter.number,
                [],
            ).append(chapter)

        resolved_chapters: list[Chapter] = []
        preferred_type: str | None = None

        for number in sorted(chapters_by_number):
            candidates = chapters_by_number[number]

            if len(candidates) == 1:
                selected = candidates[0]

            else:
                selected = next(
                    (
                        chapter
                        for chapter in candidates
                        if chapter.type == preferred_type
                    ),
                    None,
                )

                if selected is None:
                    selected = next(
                        (
                            chapter
                            for chapter in candidates
                            if chapter.type == "official"
                        ),
                        candidates[0],
                    )

            resolved_chapters.append(selected)
            preferred_type = selected.type

        return resolved_chapters
