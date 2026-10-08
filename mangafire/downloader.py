from __future__ import annotations

import subprocess


class GalleryDLNotFoundError(RuntimeError):
    """Indica que o executável gallery-dl não foi encontrado."""

    def __init__(self, executable: str) -> None:
        self.executable = executable

        super().__init__(
            f"Não foi possível encontrar o executável '{executable}'. "
            "Instale o gallery-dl e verifique se ele está disponível no PATH."
        )


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

        try:
            result = subprocess.run(
                [
                    self.executable,
                    "--cbz",
                    url,
                ],
                check=False,
            )
        except FileNotFoundError as exc:
            raise GalleryDLNotFoundError(
                executable=self.executable,
            ) from exc

        if result.returncode != 0:
            raise GalleryDLDownloadError(
                url=url,
                returncode=result.returncode,
            )
