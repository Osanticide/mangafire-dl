from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


class GalleryDLNotFoundError(RuntimeError):
    """Indica que o executável gallery-dl não foi encontrado."""

    def __init__(self, executable: str) -> None:
        self.executable = executable

        super().__init__(
            f"Could not find the gallery-dl executable "
            f"'{executable}'. Make sure gallery-dl is installed "
            "and available in PATH."
        )


class GalleryDLDownloadError(RuntimeError):
    """Indica que o gallery-dl terminou com erro."""

    def __init__(self, url: str, returncode: int) -> None:
        self.url = url
        self.returncode = returncode

        super().__init__(f"gallery-dl exited with code {returncode} for URL: {url}")


class GalleryDLArchiveNotFoundError(RuntimeError):
    """Indica que nenhum arquivo CBZ foi produzido pelo gallery-dl."""

    def __init__(self, url: str) -> None:
        self.url = url

        super().__init__(
            "gallery-dl completed successfully, but no CBZ archive "
            f"was produced for URL: {url}"
        )


class GalleryDLDownloader:
    """Executa o gallery-dl para baixar recursos do MangaFire."""

    def __init__(
        self,
        executable: str = "gallery-dl",
    ) -> None:
        self.executable = executable

    def download(
        self,
        url: str,
        destination: str | Path,
    ) -> Path:
        """Baixa uma URL usando gallery-dl e move o CBZ produzido."""

        destination = Path(destination)
        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with tempfile.TemporaryDirectory(
            prefix="mangafire-dl-",
        ) as temporary_directory:
            try:
                result = subprocess.run(
                    [
                        self.executable,
                        "--config-ignore",
                        "--cbz",
                        "-d",
                        temporary_directory,
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

            archives = sorted(
                Path(temporary_directory).rglob("*.cbz"),
            )

            if not archives:
                raise GalleryDLArchiveNotFoundError(
                    url=url,
                )

            if len(archives) > 1:
                raise GalleryDLArchiveNotFoundError(
                    url=url,
                )

            shutil.move(
                str(archives[0]),
                str(destination),
            )

        return destination
