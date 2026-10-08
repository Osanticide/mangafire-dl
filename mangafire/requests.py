from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class DownloadRequest:
    """Representa uma solicitação de download feita pelo usuário."""

    manga_url: str
    language: str
    mode: Literal["volumes", "chapters"]
    start: float
    end: float
