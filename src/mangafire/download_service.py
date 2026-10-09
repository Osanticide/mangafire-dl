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
from .parser import (
    DirectResource,
    parse_direct_resource_url,
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
    resource: Volume | Chapter | None
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

    def download_direct(
        self,
        url: str,
        progress_callback: ProgressCallback | None = None,
        output_directory: str | Path | None = None,
    ) -> None:
        """Baixa diretamente uma URL de volume ou capítulo."""

        direct_resource = parse_direct_resource_url(url)

        if direct_resource is None:
            raise ValueError("The provided URL is not a direct volume or chapter URL.")

        output_root = resolve_output_directory(
            output_directory,
        )

        manga_title = self._manga_title_from_url(
            direct_resource.manga_url,
        )

        resource_directory = (
            output_root
            / manga_title
            / ("volumes" if direct_resource.resource_type == "volume" else "chapters")
        )

        if progress_callback is not None:
            progress_callback(
                DownloadProgress(
                    index=1,
                    total=1,
                    resource=None,
                    url=url,
                    completed=False,
                )
            )

        archive = self.downloader.download_to_directory(
            url,
            resource_directory,
        )

        number = self.downloader.parse_archive_number(
            archive.name,
            direct_resource.resource_type,
        )

        if direct_resource.resource_type == "volume":
            resource = Volume(
                id=int(direct_resource.resource_id),
                number=number,
                name=f"Volume {number:g}",
                language="",
                chapter_count=0,
            )
        else:
            resource = Chapter(
                id=int(direct_resource.resource_id),
                number=number,
                name=f"Chapter {number:g}",
                language="",
                type="",
            )

        destination = build_output_path(
            output_directory=output_root,
            manga_url=direct_resource.manga_url,
            resource=resource,
        )

        archive.replace(destination)

        if progress_callback is not None:
            progress_callback(
                DownloadProgress(
                    index=1,
                    total=1,
                    resource=resource,
                    url=url,
                    completed=True,
                )
            )

    @staticmethod
    def _manga_title_from_url(
        manga_url: str,
    ) -> str:
        from .output import sanitize_path_component
        from .parser import parse_manga_title

        return sanitize_path_component(
            parse_manga_title(manga_url),
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
