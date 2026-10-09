from dataclasses import dataclass


@dataclass(frozen=True)
class Manga:
    """Representa um mangá no MangaFire."""

    id: str
    title: str


@dataclass(frozen=True)
class Volume:
    """Representa um volume de um mangá."""

    id: int
    number: float
    name: str
    language: str
    chapter_count: int


@dataclass(frozen=True)
class Chapter:
    """Representa um capítulo de um mangá."""

    id: int
    number: float
    name: str
    language: str
    type: str
