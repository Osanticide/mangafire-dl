from __future__ import annotations

import argparse
import sys

from mangafire.download_service import (
    DownloadProgress,
    MangaFireDownloadService,
)
from mangafire.downloader import GalleryDLDownloadError
from mangafire.models import Chapter, Volume
from mangafire.parser import InvalidMangaFireURLError
from mangafire.requests import (
    DownloadRequest,
    InvalidSelectionError,
    parse_selections,
)


def build_parser() -> argparse.ArgumentParser:
    """Cria o parser de argumentos da linha de comando."""

    parser = argparse.ArgumentParser(
        prog="mangafire-dl",
        description="Baixa mangás do MangaFire em formato CBZ.",
    )

    parser.add_argument(
        "url",
        help="URL do mangá no MangaFire.",
    )

    parser.add_argument(
        "--lang",
        required=True,
        help="Idioma dos volumes ou capítulos. Ex.: pt-br, en, es.",
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)

    mode_group.add_argument(
        "--volumes",
        metavar="SELEÇÃO",
        help="Volumes a baixar. Ex.: 1-5, 8, 12-15.",
    )

    mode_group.add_argument(
        "--chapters",
        metavar="SELEÇÃO",
        help="Capítulos a baixar. Ex.: 1-5, 8, 12-15.",
    )

    return parser


def show_progress(progress: DownloadProgress) -> None:
    """Exibe o progresso de um recurso no terminal."""

    resource = progress.resource

    if isinstance(resource, Volume):
        resource_type = "volume"
    elif isinstance(resource, Chapter):
        resource_type = "capítulo"
    else:
        return

    if progress.completed:
        print(
            f"[{progress.index}/{progress.total}] "
            f"✓ {resource_type.capitalize()} "
            f"{resource.number:g} concluído."
        )
    else:
        print(
            f"[{progress.index}/{progress.total}] "
            f"Baixando {resource_type} "
            f"{resource.number:g}..."
        )


def main() -> int:
    """Executa o programa."""

    parser = build_parser()
    args = parser.parse_args()

    mode = "volumes" if args.volumes is not None else "chapters"
    selection_text = args.volumes if args.volumes is not None else args.chapters

    try:
        selections = parse_selections(selection_text)

        request = DownloadRequest(
            manga_url=args.url,
            language=args.lang,
            mode=mode,
            selections=selections,
        )

        service = MangaFireDownloadService()

        service.download(
            request,
            progress_callback=show_progress,
        )

    except InvalidSelectionError as exc:
        print(f"Erro: seleção inválida: {exc}", file=sys.stderr)
        return 1

    except InvalidMangaFireURLError as exc:
        print(f"Erro: URL inválida: {exc}", file=sys.stderr)
        return 1

    except GalleryDLDownloadError as exc:
        print(f"Erro durante o download: {exc}", file=sys.stderr)
        return 1

    except Exception as exc:
        print(f"Erro inesperado: {exc}", file=sys.stderr)
        return 1

    print()
    print("Todos os downloads foram concluídos.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
