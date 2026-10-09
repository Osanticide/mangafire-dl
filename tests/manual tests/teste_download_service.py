from mangafire.download_service import (
    DownloadProgress,
    MangaFireDownloadService,
)
from mangafire.requests import (
    DownloadRequest,
    parse_selections,
)


def show_progress(progress: DownloadProgress) -> None:
    resource = progress.resource

    if isinstance(resource, type(None)):
        return

    if hasattr(resource, "number"):
        resource_type = "Volume" if hasattr(resource, "chapter_count") else "Capítulo"

        if progress.completed:
            print(
                f"[{progress.index}/{progress.total}] "
                f"✓ {resource_type} {resource.number} concluído"
            )
        else:
            print(
                f"[{progress.index}/{progress.total}] "
                f"Baixando {resource_type.lower()} "
                f"{resource.number}..."
            )


def main() -> None:
    request = DownloadRequest(
        manga_url="https://mangafire.to/title/027-bleach",
        language="pt-br",
        mode="volumes",
        selections=parse_selections("72-73"),
    )

    service = MangaFireDownloadService()

    service.download(
        request,
        progress_callback=show_progress,
    )

    print()
    print("Todos os downloads foram concluídos.")


if __name__ == "__main__":
    main()
