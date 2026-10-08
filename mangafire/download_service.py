from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .downloader import GalleryDLDownloader
from .models import Chapter, Volume
from .output import (
    build_output_path,
    resolve_output_directory,
)
from .requests import DownloadRequest
from .resolver import MangaFireResolver
from .urls import build_chapter_url, build_volume_url


class NoResourcesFoundError(RuntimeError):
    """Indica que nenhuma correspondência foi encontrada para a solicitação."""

    def __init__(
        self,
        mode: str,
        language: str,
        selections: tuple[tuple[float, float], ...],
    ) -> None:
        self.mode = mode
        self.language = language
        self.selections = selections

        super().__init__(
            "Nenhum recurso foi encontrado para a seleção informada "
            f"(modo: {mode}, idioma: {language})."
        )


@dataclass(frozen=True)
class DownloadProgress:
    """Representa o progresso de um recurso durante o download."""

    index: int
    total: int
    resource: Volume | Chapter
    url: str
    completed: bool


ProgressCallback = Callable[[DownloadProgress], None]


class MangaFireDownloadService:
    """Coordena a resolução e o download de recursos do MangaFire."""

    def __init__(
        self,
        resolver: MangaFireResolver | None = None,
        downloader: GalleryDLDownloader | None = None,
    ) -> None:
        self.resolver = resolver or MangaFireResolver()
        self.downloader = downloader or GalleryDLDownloader()

    def download(
        self,
        request: DownloadRequest,
        progress_callback: ProgressCallback | None = None,
        output_directory: str | Path | None = None,
    ) -> None:
        """Resolve e baixa todos os recursos da solicitação em sequência."""

        resources = self.resolver.resolve_request(request)

        if not resources:
            raise NoResourcesFoundError(
                mode=request.mode,
                language=request.language,
                selections=request.selections,
            )

        output_root = resolve_output_directory(
            output_directory,
        )

        total = len(resources)

        for index, resource in enumerate(resources, start=1):
            url = self._build_url(
                request.manga_url,
                resource,
            )

            destination = build_output_path(
                output_directory=output_root,
                manga_url=request.manga_url,
                resource=resource,
            )

            if progress_callback is not None:
                progress_callback(
                    DownloadProgress(
                        index=index,
                        total=total,
                        resource=resource,
                        url=url,
                        completed=False,
                    )
                )

            self.downloader.download(
                url,
                destination,
            )

            if progress_callback is not None:
                progress_callback(
                    DownloadProgress(
                        index=index,
                        total=total,
                        resource=resource,
                        url=url,
                        completed=True,
                    )
                )

    @staticmethod
    def _build_url(
        manga_url: str,
        resource: Volume | Chapter,
    ) -> str:
        """Constrói a URL correspondente ao recurso."""

        if isinstance(resource, Volume):
            return build_volume_url(
                manga_url,
                resource,
            )

        if isinstance(resource, Chapter):
            return build_chapter_url(
                manga_url,
                resource,
            )

        raise TypeError(f"Tipo de recurso não suportado: {type(resource).__name__}")
