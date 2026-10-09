from __future__ import annotations

import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

# automação de build

ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "src" / "mangafire" / "version.py"
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"
STAGE_DIR = BUILD_DIR / "release-stage"


def read_version() -> str:
    """Reads the project version from version.py."""
    content = VERSION_FILE.read_text(encoding="utf-8")

    match = re.search(
        r"""__version__\s*=\s*["']([^"']+)["']""",
        content,
    )

    if match is None:
        raise RuntimeError(f"Could not read project version from {VERSION_FILE}")

    return match.group(1)


def run_step(label: str, command: list[str]) -> None:
    """Runs a build step and stops if it fails."""
    print(f"\n{'=' * 60}", flush=True)
    print(label, flush=True)
    print(f"{'=' * 60}", flush=True)

    subprocess.run(
        command,
        cwd=ROOT,
        check=True,
    )


def prepare_stage() -> None:
    """Creates a clean staging directory for this build."""
    if STAGE_DIR.exists():
        shutil.rmtree(STAGE_DIR)

    STAGE_DIR.mkdir(parents=True)


def build_python_packages(version: str) -> list[Path]:
    """Builds and validates the wheel and source distribution."""
    output_dir = STAGE_DIR / "python"
    output_dir.mkdir(parents=True)

    run_step(
        "Running Python package tests",
        [sys.executable, "-m", "pytest"],
    )

    run_step(
        "Building wheel and source distribution",
        [
            sys.executable,
            "-m",
            "build",
            "--sdist",
            "--wheel",
            "--outdir",
            str(output_dir),
        ],
    )

    wheels = list(output_dir.glob(f"mangafire_dl-{version}-*.whl"))
    source_distributions = list(output_dir.glob(f"mangafire_dl-{version}.tar.gz"))

    if len(wheels) != 1:
        raise RuntimeError(
            f"Expected one wheel for version {version}, found {len(wheels)}."
        )

    if len(source_distributions) != 1:
        raise RuntimeError(
            f"Expected one source distribution for version {version}, "
            f"found {len(source_distributions)}."
        )

    return [wheels[0], source_distributions[0]]


def windows_architecture() -> str:
    """Returns a recognizable Windows architecture label."""
    machine = platform.machine().lower()

    architectures = {
        "amd64": "x64",
        "x86_64": "x64",
        "arm64": "arm64",
        "aarch64": "arm64",
        "x86": "x86",
        "i386": "x86",
        "i686": "x86",
    }

    return architectures.get(machine, machine or "unknown")


def build_windows_standalone(version: str) -> tuple[Path, Path]:
    """Builds the Windows standalone folder and its ZIP archive."""
    source_main = ROOT / "main.py"
    launcher_template = ROOT / "packaging" / "windows" / "Executar.bat"

    if not launcher_template.is_file():
        raise RuntimeError(f"Windows launcher template not found: {launcher_template}")

    template = launcher_template.read_text(encoding="utf-8")

    if "@VERSION@" not in template:
        raise RuntimeError("Executar.bat must contain the @VERSION@ placeholder.")

    standalone_dir = STAGE_DIR / "standalone"

    run_step(
        "Building Windows standalone with PyInstaller",
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--clean",
            "--noconfirm",
            "--onedir",
            "--name",
            "mangafire-dl",
            "--paths",
            str(ROOT / "src"),
            "--collect-all",
            "gallery_dl",
            "--distpath",
            str(standalone_dir),
            "--workpath",
            str(BUILD_DIR / "pyinstaller-work"),
            "--specpath",
            str(BUILD_DIR / "pyinstaller-spec"),
            str(source_main),
        ],
    )

    app_dir = standalone_dir / "mangafire-dl"
    executable = app_dir / "mangafire-dl.exe"

    if not executable.is_file():
        raise RuntimeError(
            f"PyInstaller did not produce the expected executable: {executable}"
        )

    launcher_content = template.replace("@VERSION@", version)

    (app_dir / "Executar.bat").write_text(
        launcher_content,
        encoding="utf-8",
        newline="\r\n",
    )

    archive_name = f"mangafire-dl-windows-{windows_architecture()}-{version}"

    archive = Path(
        shutil.make_archive(
            str(STAGE_DIR / archive_name),
            "zip",
            root_dir=str(standalone_dir),
            base_dir="mangafire-dl",
        )
    )

    return app_dir, archive


def publish_local_artifacts(
    python_packages: list[Path],
    windows_artifacts: tuple[Path, Path] | None,
) -> list[Path]:
    """Copies successful staged artifacts into dist/."""
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    published = []

    for artifact in python_packages:
        destination = DIST_DIR / artifact.name
        shutil.copy2(artifact, destination)
        published.append(destination)

    if windows_artifacts is not None:
        standalone_dir, archive = windows_artifacts
        destination_dir = DIST_DIR / "standalone" / "mangafire-dl"

        if destination_dir.exists():
            shutil.rmtree(destination_dir)

        destination_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(standalone_dir, destination_dir)

        archive_destination = DIST_DIR / archive.name
        shutil.copy2(archive, archive_destination)

        published.extend([destination_dir, archive_destination])

    return published


def main() -> int:
    try:
        version = read_version()

        print(f"MangaFire Downloader release build: {version}")
        print(f"Platform: {platform.system()}")

        # Tests must pass before we build any release artifacts.
        run_step(
            "Running test suite",
            [sys.executable, "-m", "pytest"],
        )

        prepare_stage()

        # The package formats are platform-independent for this project.
        run_step(
            "Building wheel and source distribution",
            [
                sys.executable,
                "-m",
                "build",
                "--sdist",
                "--wheel",
                "--outdir",
                str(STAGE_DIR / "python"),
            ],
        )

        python_output = STAGE_DIR / "python"
        python_output.mkdir(exist_ok=True)

        wheels = list(python_output.glob(f"mangafire_dl-{version}-*.whl"))
        source_distributions = list(
            python_output.glob(f"mangafire_dl-{version}.tar.gz")
        )

        if len(wheels) != 1 or len(source_distributions) != 1:
            raise RuntimeError(
                "Could not validate the wheel and source distribution "
                f"for version {version}."
            )

        python_packages = [wheels[0], source_distributions[0]]
        windows_artifacts = None

        if platform.system() == "Windows":
            windows_artifacts = build_windows_standalone(version)
        else:
            print(
                "\nSkipping Windows standalone: "
                "run this script on Windows to build the Windows ZIP."
            )

        published = publish_local_artifacts(
            python_packages,
            windows_artifacts,
        )

        print("\nBuild completed successfully.")
        print("Artifacts:")

        for artifact in published:
            print(f"  {artifact.relative_to(ROOT)}")

        return 0

    except subprocess.CalledProcessError as exc:
        print(
            f"\nBuild failed: a command exited with code {exc.returncode}.",
            file=sys.stderr,
        )
        return exc.returncode or 1

    except (OSError, RuntimeError) as exc:
        print(f"\nBuild failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
