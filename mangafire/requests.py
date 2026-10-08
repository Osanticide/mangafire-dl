from dataclasses import dataclass
import math
import re
from typing import Literal, TypeAlias


Selection: TypeAlias = tuple[float, float]


class InvalidSelectionError(ValueError):
    """Indica que uma seleção de capítulos ou volumes é inválida."""


def parse_selections(value: str) -> tuple[Selection, ...]:
    """Converte uma seleção textual em uma sequência de intervalos."""

    if not value.strip():
        raise InvalidSelectionError("A seleção não pode estar vazia.")

    parts = re.split(r"[;,]", value)
    selections: list[Selection] = []

    for part in parts:
        part = part.strip()

        if not part:
            raise InvalidSelectionError("A seleção contém um item vazio.")

        if part.count("-") > 1:
            raise InvalidSelectionError(f"Seleção inválida: {part}")

        if "-" in part:
            start_text, end_text = part.split("-", 1)

            if not start_text.strip() or not end_text.strip():
                raise InvalidSelectionError(f"Intervalo inválido: {part}")

            try:
                start = float(start_text.strip())
                end = float(end_text.strip())
            except ValueError as exc:
                raise InvalidSelectionError(f"Seleção inválida: {part}") from exc

        else:
            try:
                start = float(part)
                end = start
            except ValueError as exc:
                raise InvalidSelectionError(f"Seleção inválida: {part}") from exc

        if not math.isfinite(start) or not math.isfinite(end):
            raise InvalidSelectionError(f"Seleção inválida: {part}")

        if start > end:
            raise InvalidSelectionError(
                f"O início não pode ser maior que o fim: {part}"
            )

        selections.append((start, end))

    return tuple(selections)


@dataclass(frozen=True)
class DownloadRequest:
    """Representa uma solicitação de download feita pelo usuário."""

    manga_url: str
    language: str
    mode: Literal["volumes", "chapters"]
    selections: tuple[Selection, ...]
