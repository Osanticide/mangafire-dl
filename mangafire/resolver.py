from __future__ import annotations

from .api import MangaFireAPI
from .models import Chapter, Volume
from .parser import parse_manga_id
from .requests import DownloadRequest, Selection


class InvalidVolumeRangeError(ValueError):
    """Indica que o intervalo de volumes é inválido."""


class InvalidChapterRangeError(ValueError):
    """Indica que o intervalo de capítulos é inválido."""


class MangaFireResolver:
    """Resolve recursos do MangaFire a partir dos critérios do usuário."""

    def __init__(self, api: MangaFireAPI | None = None) -> None:
        self.api = api or MangaFireAPI()

    @staticmethod
    def _matches_selection(
        number: float,
        selections: tuple[Selection, ...],
    ) -> bool:
        """Verifica se um número pertence a alguma das seleções."""

        return any(start <= number <= end for start, end in selections)

    def resolve_request(
        self,
        request: DownloadRequest,
    ) -> list[Volume | Chapter]:
        """Resolve uma solicitação de download."""

        manga_id = parse_manga_id(request.manga_url)

        if request.mode == "volumes":
            return self.resolve_volumes(
                manga_id=manga_id,
                language=request.language,
                selections=request.selections,
            )

        if request.mode == "chapters":
            return self.resolve_chapters(
                manga_id=manga_id,
                language=request.language,
                selections=request.selections,
            )

        raise ValueError(f"Modo de download inválido: {request.mode}")

    def resolve_volumes(
        self,
        manga_id: str,
        language: str,
        selections: tuple[Selection, ...],
    ) -> list[Volume]:
        """Resolve volumes conforme as seleções e o idioma."""

        if not selections:
            raise InvalidVolumeRangeError("Nenhuma seleção de volumes foi informada.")

        volumes = self.api.get_volumes(manga_id)

        matching_volumes = [
            volume
            for volume in volumes
            if (
                volume.language == language
                and self._matches_selection(
                    volume.number,
                    selections,
                )
            )
        ]

        return sorted(
            matching_volumes,
            key=lambda volume: volume.number,
        )

    def resolve_chapters(
        self,
        manga_id: str,
        language: str,
        selections: tuple[Selection, ...],
    ) -> list[Chapter]:
        """Resolve capítulos conforme as seleções e o idioma."""

        if not selections:
            raise InvalidChapterRangeError(
                "Nenhuma seleção de capítulos foi informada."
            )

        chapters = self.api.get_chapters(
            manga_id,
            language=language,
        )

        matching_chapters = [
            chapter
            for chapter in chapters
            if self._matches_selection(
                chapter.number,
                selections,
            )
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
