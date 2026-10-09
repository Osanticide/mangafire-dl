from __future__ import annotations

import re
import shutil
import tempfile
from pathlib import Path

from gallery_dl import config, job


class GalleryDLNotFoundError(RuntimeError):
    """Indica que o módulo gallery-dl não está disponível."""

    def __init__(self, executable: str = "gallery-dl") -> None:
        self.executable = executable
        super().__init__(f"Could not find the gallery-dl dependency '{executable}'.")


class GalleryDLDownloadError(RuntimeError):
    """Indica que o gallery-dl terminou com erro."""

    def __init__(self, url: str, returncode: int) -> None:
        self.url = url
        self.returncode = returncode

        super().__init__(f"gallery-dl exited with code {returncode} for URL: {url}")


class GalleryDLArchiveNotFoundError(RuntimeError):
    """Indica que não foi produzido exatamente um arquivo CBZ."""

    def __init__(self, url: str) -> None:
        self.url = url

        super().__init__(
            f"gallery-dl did not produce exactly one CBZ archive for URL: {url}"
        )


class GalleryDLArchiveNameError(RuntimeError):
    """Indica que o nome do CBZ não pôde ser interpretado."""

    def __init__(
        self,
        archive_name: str,
        resource_type: str,
    ) -> None:
        self.archive_name = archive_name
        self.resource_type = resource_type

        super().__init__(
            f"Could not determine the {resource_type} number "
            f"from gallery-dl archive name: {archive_name}"
        )


class GalleryDLDownloader:
    """Executa o gallery-dl como biblioteca Python."""

    def download(
        self,
        url: str,
        destination: str | Path,
    ) -> Path:
        """Baixa uma URL e move o CBZ para o caminho de destino."""

        destination = Path(destination)
        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with tempfile.TemporaryDirectory(
            prefix="mangafire-dl-",
        ) as temporary_directory:
            archive = self._download_archive(
                url,
                temporary_directory,
            )

            shutil.move(
                str(archive),
                str(destination),
            )

        return destination

    def download_to_directory(
        self,
        url: str,
        destination_directory: str | Path,
    ) -> Path:
        """Baixa uma URL e preserva o nome original do CBZ."""

        destination_directory = Path(destination_directory)
        destination_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        with tempfile.TemporaryDirectory(
            prefix="mangafire-dl-",
        ) as temporary_directory:
            archive = self._download_archive(
                url,
                temporary_directory,
            )

            destination = destination_directory / archive.name

            shutil.move(
                str(archive),
                str(destination),
            )

        return destination

    @staticmethod
    def _download_archive(
        url: str,
        temporary_directory: str | Path,
    ) -> Path:
        """Executa o download em um ambiente de configuração controlado."""

        # Não carrega os arquivos de configuração pessoais do gallery-dl.
        config.clear()

        config.set(
            ("extractor",),
            "base-directory",
            str(temporary_directory),
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

        download_job = job.DownloadJob(url)
        returncode = download_job.run()

        if returncode != 0:
            raise GalleryDLDownloadError(
                url=url,
                returncode=returncode,
            )

        archives = sorted(
            Path(temporary_directory).rglob("*.cbz"),
        )

        if len(archives) != 1:
            raise GalleryDLArchiveNotFoundError(url)

        return archives[0]

    @staticmethod
    def parse_archive_number(
        archive_name: str,
        resource_type: str,
    ) -> float:
        """Extrai o número do recurso do nome produzido pelo gallery-dl."""

        if resource_type == "volume":
            pattern = r"^v(?P<number>\d+(?:\.\d+)?)\.cbz$"
        elif resource_type == "chapter":
            pattern = r"^c(?P<number>\d+(?:\.\d+)?)(?:_.*)?\.cbz$"
        else:
            raise ValueError(f"Unsupported resource type: {resource_type}")

        match = re.match(
            pattern,
            archive_name,
            re.IGNORECASE,
        )

        if match is None:
            raise GalleryDLArchiveNameError(
                archive_name=archive_name,
                resource_type=resource_type,
            )

        return float(match.group("number"))
