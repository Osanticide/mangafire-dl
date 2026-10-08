from __future__ import annotations

from .models import Chapter, Volume


def build_volume_url(manga_url: str, volume: Volume) -> str:
    """Monta a URL de leitura de um volume do MangaFire."""
    return f"{manga_url.rstrip('/')}/volume/{volume.id}"


def build_chapter_url(manga_url: str, chapter: Chapter) -> str:
    """Monta a URL de leitura de um capítulo do MangaFire."""
    return f"{manga_url.rstrip('/')}/chapter/{chapter.id}"
