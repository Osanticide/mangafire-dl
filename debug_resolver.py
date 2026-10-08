from collections import Counter

from mangafire.api import MangaFireAPI
from mangafire.resolver import MangaFireResolver


api = MangaFireAPI()
resolver = MangaFireResolver(api)


chapters = resolver.resolve_chapters(
    manga_id="027",
    language="en",
    start=1,
    end=1458,
)


print(f"Total de capítulos resolvidos: {len(chapters)}")

types = Counter(chapter.type for chapter in chapters)

print("\nTipos escolhidos:")
for chapter_type, count in sorted(types.items()):
    print(f"  {chapter_type}: {count}")


print("\nPrimeiros 20 capítulos:")
for chapter in chapters[:20]:
    print(
        f"  Capítulo {chapter.number}: "
        f"ID={chapter.id} "
        f"type={chapter.type} "
        f"name={chapter.name!r}"
    )


print("\nÚltimos 10 capítulos:")
for chapter in chapters[-10:]:
    print(
        f"  Capítulo {chapter.number}: "
        f"ID={chapter.id} "
        f"type={chapter.type} "
        f"name={chapter.name!r}"
    )


print("\nMudanças de preferência:")

previous_type = None

for chapter in chapters:
    if previous_type is not None and chapter.type != previous_type:
        print(f"  Capítulo {chapter.number}: {previous_type} -> {chapter.type}")

    previous_type = chapter.type
