from collections import Counter

from mangafire.api import MangaFireAPI
from mangafire.resolver import MangaFireResolver


api = MangaFireAPI()
resolver = MangaFireResolver(api)


raw_chapters = api.get_chapters(
    "027",
    language="en",
)

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


raw_counts = Counter(chapter.number for chapter in raw_chapters)

print("\nNúmeros com mais de duas entradas:")

found_extra_entries = False

for number, count in sorted(raw_counts.items()):
    if count > 2:
        found_extra_entries = True
        print(f"  Capítulo {number}: {count} entradas")

if not found_extra_entries:
    print("  Nenhum.")

print("\nNúmeros fora do intervalo 1-1458:")

outside_range = sorted(
    {chapter.number for chapter in raw_chapters if not 1 <= chapter.number <= 1458}
)

if outside_range:
    for number in outside_range:
        print(f"  Capítulo {number}")
else:
    print("  Nenhum.")


print("\nMenor e maior número encontrados:")

numbers = [chapter.number for chapter in raw_chapters]

print(f"  Menor: {min(numbers)}")
print(f"  Maior: {max(numbers)}")
