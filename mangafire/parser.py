from urllib.parse import urlsplit


class InvalidMangaFireURLError(ValueError):
    """Indica que a URL fornecida não é uma URL válida do MangaFire."""


def parse_manga_id(url: str) -> str:
    """Extrai o ID do mangá de uma URL do MangaFire."""
    parsed = urlsplit(url)

    if parsed.scheme not in ("http", "https"):
        raise InvalidMangaFireURLError("A URL deve usar http ou https.")

    if parsed.netloc != "mangafire.to":
        raise InvalidMangaFireURLError("A URL não pertence ao MangaFire.")

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2 or parts[0] != "title":
        raise InvalidMangaFireURLError("A URL não é uma URL de título do MangaFire.")

    manga_id = parts[1].split("-", 1)[0]

    if not manga_id:
        raise InvalidMangaFireURLError("Não foi possível identificar o mangá.")

    return manga_id
