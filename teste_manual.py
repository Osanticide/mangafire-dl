from mangafire.requests import DownloadRequest
from mangafire.resolver import MangaFireResolver
from mangafire.urls import build_chapter_url, build_volume_url


def read_range() -> tuple[float, float]:
    while True:
        value = input("Intervalo (ex.: 1-10): ").strip()

        try:
            start, end = value.split("-", 1)
            start = float(start.strip())
            end = float(end.strip())

            if start > end:
                print("O início não pode ser maior que o fim.")
                continue

            return start, end

        except ValueError:
            print("Intervalo inválido. Use o formato: 1-10")


def main() -> None:
    print("=" * 60)
    print("MangaFire Downloader - Teste manual")
    print("=" * 60)

    manga_url = input("\nURL do mangá: ").strip()

    language = input("Idioma (ex.: pt-br, en, es): ").strip()

    while True:
        mode = input("Baixar [v]olumes ou [c]apítulos? ").strip().lower()

        if mode == "v":
            mode = "volumes"
            break

        if mode == "c":
            mode = "chapters"
            break

        print("Digite 'v' para volumes ou 'c' para capítulos.")

    start, end = read_range()

    request = DownloadRequest(
        manga_url=manga_url,
        language=language,
        mode=mode,
        start=start,
        end=end,
    )

    print("\nResolvendo...\n")

    resolver = MangaFireResolver()
    resources = resolver.resolve_request(request)

    if not resources:
        print("Nenhum resultado encontrado.")
        return

    print(f"Encontrados: {len(resources)}")
    print()

    for resource in resources:
        if mode == "volumes":
            url = build_volume_url(manga_url, resource)

            print(
                f"Volume {resource.number} | "
                f"ID: {resource.id} | "
                f"Idioma: {resource.language}"
            )

        else:
            url = build_chapter_url(manga_url, resource)

            print(
                f"Capítulo {resource.number} | "
                f"ID: {resource.id} | "
                f"Tipo: {resource.type}"
            )

        print(f"  URL: {url}")
        print()


if __name__ == "__main__":
    main()
