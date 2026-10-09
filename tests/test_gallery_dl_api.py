import tempfile
from pathlib import Path

from gallery_dl import config, job

URL = "https://mangafire.to/title/027-bleach/volume/144857"


def main():
    with tempfile.TemporaryDirectory(
        prefix="mangafire-dl-test-"
    ) as temporary_directory:
        output_dir = Path(temporary_directory)

        print(f"Diretório temporário: {output_dir}")

        config.clear()
        config.set(
            ("extractor",),
            "base-directory",
            str(output_dir),
        )
        config.set(
            ("extractor",),
            "postprocessors",
            [
                {
                    "name": "zip",
                    "extension": "cbz",
                }
            ],
        )

        print("Iniciando download...")
        job.DownloadJob(URL).run()

        files = list(output_dir.rglob("*"))
        archives = [
            path for path in files if path.is_file() and path.suffix.lower() == ".cbz"
        ]

        print(f"Arquivos CBZ encontrados: {len(archives)}")

        for archive in archives:
            print(f"  {archive.name}")

        if len(archives) != 1:
            raise RuntimeError(f"Esperado 1 arquivo CBZ, encontrados {len(archives)}.")

        print("Teste concluído com sucesso.")

    print("Diretório temporário removido.")


if __name__ == "__main__":
    main()
