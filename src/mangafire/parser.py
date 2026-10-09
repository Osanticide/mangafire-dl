from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import unquote, urlsplit


class InvalidMangaFireURLError(ValueError):
    """Indica que a URL fornecida não é uma URL válida do MangaFire."""


@dataclass(frozen=True)
class DirectResource:
    """Representa uma URL direta de volume ou capítulo."""

    url: str
    manga_url: str
    resource_type: str
    resource_id: str


def _parse_title_identifier(url: str) -> str:
    """Extrai o identificador do título da URL."""

    parsed = urlsplit(url)

    if parsed.scheme not in ("http", "https"):
        raise InvalidMangaFireURLError("A URL deve usar http ou https.")

    if parsed.netloc != "mangafire.to":
        raise InvalidMangaFireURLError("A URL não pertence ao MangaFire.")

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2 or parts[0] != "title":
        raise InvalidMangaFireURLError("A URL não é uma URL de título do MangaFire.")

    identifier = unquote(parts[1])

    if not identifier:
        raise InvalidMangaFireURLError("Não foi possível identificar o mangá.")

    return identifier


def parse_manga_id(url: str) -> str:
    """Extrai o ID do mangá de uma URL do MangaFire."""

    identifier = _parse_title_identifier(url)

    manga_id = identifier.split("-", 1)[0]

    if not manga_id:
        raise InvalidMangaFireURLError("Não foi possível identificar o mangá.")

    return manga_id


def parse_manga_title(url: str) -> str:
    """Extrai o título legível do mangá a partir da URL."""

    identifier = _parse_title_identifier(url)

    parts = identifier.split("-", 1)

    if len(parts) == 1 or not parts[1]:
        return parts[0]

    slug = parts[1]

    words = [word for word in slug.split("-") if word]

    if not words:
        return parts[0]

    return " ".join(word.capitalize() for word in words)


def parse_direct_resource_url(
    url: str,
) -> DirectResource | None:
    """Identifica uma URL direta de volume ou capítulo.

    Retorna None quando a URL é apenas uma URL de título.
    """

    parsed = urlsplit(url)

    if parsed.scheme not in ("http", "https"):
        raise InvalidMangaFireURLError("A URL deve usar http ou https.")

    if parsed.netloc != "mangafire.to":
        raise InvalidMangaFireURLError("A URL não pertence ao MangaFire.")

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2 or parts[0] != "title":
        raise InvalidMangaFireURLError("A URL não é uma URL de título do MangaFire.")

    identifier = unquote(parts[1])

    if not identifier:
        raise InvalidMangaFireURLError("Não foi possível identificar o mangá.")

    if len(parts) == 2:
        return None

    if len(parts) != 4 or parts[2] not in ("volume", "chapter"):
        raise InvalidMangaFireURLError(
            "A URL não é uma URL direta válida de volume ou capítulo."
        )

    resource_id = unquote(parts[3])

    if not resource_id:
        raise InvalidMangaFireURLError("Não foi possível identificar o recurso.")

    manga_url = f"{parsed.scheme}://{parsed.netloc}/title/{identifier}"

    return DirectResource(
        url=url,
        manga_url=manga_url,
        resource_type=parts[2],
        resource_id=resource_id,
    )
