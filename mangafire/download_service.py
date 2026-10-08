from __future__ import annotations

from .downloader import GalleryDLDownloader
from .models import Chapter, Volume
from .requests import DownloadRequest
from .resolver import MangaFireResolver
from .urls import build_chapter_url, build_volume_url


class MangaFireDownloadService:
    """Coordena a resolução e o download de recursos do MangaFire."""

    def __init__(
        self,
        resolver: MangaFireResolver | None = None,
        downloader: GalleryDLDownloader | None = None,
    ) -> None:
        self.resolver = resolver or MangaFireResolver()
        self.downloader = downloader or GalleryDLDownloader()

    def download(self, request: DownloadRequest) -> None:
        """Resolve e baixa todos os recursos da solicitação em sequência."""

        resources = self.resolver.resolve_request(request)

        for resource in resources:
            url = self._build_url(request.manga_url, resource)
            self.downloader.download(url)

    @staticmethod
    def _build_url(
        manga_url: str,
        resource: Volume | Chapter,
    ) -> str:
        """Constrói a URL correspondente ao recurso."""

        if isinstance(resource, Volume):
            return build_volume_url(manga_url, resource)

        if isinstance(resource, Chapter):
            return build_chapter_url(manga_url, resource)

        raise TypeError(f"Tipo de recurso não suportado: {type(resource).__name__}")
