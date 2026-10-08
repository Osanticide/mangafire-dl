from __future__ import annotations

import subprocess


class GalleryDLDownloadError(RuntimeError):
    """Indica que o gallery-dl terminou com erro."""

    def __init__(self, url: str, returncode: int) -> None:
        self.url = url
        self.returncode = returncode

        super().__init__(
            f"gallery-dl terminou com código de saída {returncode} para a URL: {url}"
        )


class GalleryDLDownloader:
    """Executa o gallery-dl para baixar recursos do MangaFire."""

    def __init__(self, executable: str = "gallery-dl") -> None:
        self.executable = executable

    def download(self, url: str) -> None:
        """Baixa uma URL usando gallery-dl e gera um CBZ."""

        result = subprocess.run(
            [
                self.executable,
                "--cbz",
                url,
            ],
            check=False,
        )

        if result.returncode != 0:
            raise GalleryDLDownloadError(
                url=url,
                returncode=result.returncode,
            )
