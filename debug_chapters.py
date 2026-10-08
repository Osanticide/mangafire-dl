from collections import Counter, defaultdict

from mangafire.api import MangaFireAPI


LANGUAGES = [
    "pt-br",
    "en",
    "es",
    "es-419",
    "fr",
]


api = MangaFireAPI()


for language in LANGUAGES:
    print("=" * 60)
    print(f"IDIOMA: {language}")
    print("=" * 60)

    chapters = api.get_chapters(
        "027",
        language=language,
    )

    print(f"Total: {len(chapters)}")

    types = Counter(chapter.type for chapter in chapters)

    print("\nTipos:")
    for chapter_type, count in sorted(types.items()):
        print(f"  {chapter_type}: {count}")

    by_number = defaultdict(list)

    for chapter in chapters:
        by_number[chapter.number].append(chapter)

    duplicates = {
        number: items for number, items in by_number.items() if len(items) > 1
    }

    print(f"\nCapítulos com mais de uma entrada: {len(duplicates)}")

    if duplicates:
        print("\nExemplos de duplicados:")

        for number, items in sorted(duplicates.items())[:10]:
            print(f"\n  Capítulo {number}:")

            for chapter in items:
                print(f"    ID={chapter.id} type={chapter.type} name={chapter.name!r}")

    print()
