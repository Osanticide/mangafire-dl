from __future__ import annotations

import re
from pathlib import Path

from .models import Chapter, Volume
from .parser import parse_manga_title


def resolve_output_directory(
    output_directory: str | Path | None,
) -> Path:
    """Resolve o diretório raiz de saída."""

    if output_directory is None:
        return Path.home() / "Downloads"

    return Path(output_directory).expanduser()


def sanitize_path_component(value: str) -> str:
    """Remove caracteres inválidos para nomes de arquivos e diretórios."""

    sanitized = re.sub(r'[<>:"/\\|?*]', "", value)
    sanitized = sanitized.strip().rstrip(".")

    return sanitized or "Unknown"


def format_resource_number(
    number: float,
    width: int,
) -> str:
    """Formata o número de um volume ou capítulo."""

    if number.is_integer():
        return f"{int(number):0{width}d}"

    return str(number)


def build_output_path(
    output_directory: str | Path,
    manga_url: str,
    resource: Volume | Chapter,
) -> Path:
    """Constrói o caminho final de um recurso baixado."""

    output_directory = Path(output_directory)

    manga_title = sanitize_path_component(
        parse_manga_title(manga_url),
    )

    if isinstance(resource, Volume):
        resource_number = format_resource_number(
            resource.number,
            width=2,
        )

        filename = f"{manga_title} - Volume {resource_number}.cbz"

        return output_directory / manga_title / "volumes" / filename

    if isinstance(resource, Chapter):
        resource_number = format_resource_number(
            resource.number,
            width=3,
        )

        filename = f"{manga_title} - Chapter {resource_number}.cbz"

        return output_directory / manga_title / "chapters" / filename

    raise TypeError(f"Unsupported resource type: {type(resource).__name__}")
