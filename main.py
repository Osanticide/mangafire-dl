from __future__ import annotations

import argparse
import sys

import requests

from mangafire.download_service import (
    DownloadProgress,
    MangaFireDownloadService,
    NoResourcesFoundError,
)
from mangafire.downloader import (
    GalleryDLDownloadError,
    GalleryDLNotFoundError,
)
from mangafire.models import Chapter, Volume
from mangafire.parser import InvalidMangaFireURLError
from mangafire.requests import (
    DownloadRequest,
    InvalidSelectionError,
    parse_selections,
)
from mangafire.version import __version__


def build_parser() -> argparse.ArgumentParser:
    """Creates the command-line argument parser."""

    parser = argparse.ArgumentParser(
        prog="mangafire-dl",
        description=(
            "Download manga volumes and chapters from MangaFire "
            "in CBZ format using gallery-dl."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  mangafire-dl URL --lang pt-br --volumes 1-5\n"
            "  mangafire-dl URL --lang pt-br --volumes 1, 6, 12\n"
            "  mangafire-dl URL --lang en --chapters 1-20\n"
            "  mangafire-dl URL --lang en --chapters 1-5, 10, 12-15"
        ),
    )

    parser.add_argument(
        "url",
        help="MangaFire manga URL.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "--lang",
        required=True,
        metavar="LANGUAGE",
        help="Language of the volumes or chapters. E.g.: pt-br, en, es.",
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)

    mode_group.add_argument(
        "--volumes",
        metavar="SELECTION",
        help=(
            "Volumes to download. "
            "Accepts numbers, ranges, and lists. "
            "E.g.: 1-5, 8, 12-15."
        ),
    )

    mode_group.add_argument(
        "--chapters",
        metavar="SELECTION",
        help=(
            "Chapters to download. "
            "Accepts numbers, ranges, and lists. "
            "E.g.: 1-5, 8, 12-15."
        ),
    )

    return parser


def show_progress(progress: DownloadProgress) -> None:
    """Displays resource download progress in the terminal."""

    resource = progress.resource

    if isinstance(resource, Volume):
        resource_type = "volume"
    elif isinstance(resource, Chapter):
        resource_type = "chapter"
    else:
        return

    if progress.completed:
        print(
            f"[{progress.index}/{progress.total}] "
            f"✓ {resource_type.capitalize()} "
            f"{resource.number:g} completed."
        )
    else:
        print(
            f"[{progress.index}/{progress.total}] "
            f"Downloading {resource_type} "
            f"{resource.number:g}..."
        )


def main() -> int:
    """Runs the application."""

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
        print(
            f"Selection error: {exc}",
            file=sys.stderr,
        )
        return 1

    except InvalidMangaFireURLError as exc:
        print(
            f"URL error: {exc}",
            file=sys.stderr,
        )
        return 1

    except NoResourcesFoundError as exc:
        print(
            f"Error: {exc}",
            file=sys.stderr,
        )
        return 1

    except GalleryDLNotFoundError as exc:
        print(
            f"Error: {exc}",
            file=sys.stderr,
        )
        return 1

    except GalleryDLDownloadError as exc:
        print(
            f"Download error: {exc}",
            file=sys.stderr,
        )
        return 1

    except requests.RequestException as exc:
        print(
            f"MangaFire communication error: {exc}",
            file=sys.stderr,
        )
        return 1

    except Exception as exc:
        print(
            f"Unexpected error: {exc}",
            file=sys.stderr,
        )
        return 1

    print()
    print("All downloads completed successfully.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
