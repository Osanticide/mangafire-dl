[English](README.md) | [Português](README.pt.md)

# MangaFire Downloader

A command-line tool for downloading manga volumes and chapters from MangaFire as CBZ archives.

**Built on [`gallery-dl`](https://github.com/mikf/gallery-dl).** MangaFire Downloader relies on the `gallery-dl` project for its underlying extraction and download capabilities. This project would not exist in its current form without the work of the `gallery-dl` developers and contributors.

> **Latest release:** [v0.5.0](https://github.com/Osanticide/mangafire-dl/releases/tag/v0.5.0). Install from [PyPI](https://pypi.org/project/mangafire-dl/) or download the [Windows portable ZIP](https://github.com/Osanticide/mangafire-dl/releases/download/v0.5.0/mangafire-dl-windows-x64-0.5.0.zip).

## Features

- Download individual volumes or chapters directly from their MangaFire URLs.
- Select volumes or chapters from a manga page by number, range, or a combination of both.
- Save downloads as CBZ archives.
- Choose a custom output directory.
- Use the command-line interface on supported Python environments or the portable Windows build without installing Python.

## Installation

### Windows — Portable ZIP

1. Open [GitHub Releases](https://github.com/Osanticide/mangafire-dl/releases).
2. Download the `mangafire-dl-windows-x64-<version>.zip` asset for the release you want.
3. Extract the ZIP to a folder.
4. To use the guided prompt, double-click `Executar.bat`. It asks for the MangaFire URL and the download options, then keeps the terminal open so you can read the result.
5. To use the command-line interface directly, run `mangafire-dl.exe` from PowerShell or Command Prompt and pass the URL and options shown below.

The portable ZIP includes the executable and its required files. Keep `mangafire-dl.exe`, `Executar.bat`, and the `_internal` directory together. Do not move or distribute the EXE by itself.

### Python — pipx

After the package is published on PyPI, install the command-line application with:

```powershell
pipx install mangafire-dl
```

To upgrade it later:

```powershell
pipx upgrade mangafire-dl
```

### Python — pip

Python 3.10 or newer is required. Using a virtual environment is recommended:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install mangafire-dl
```

On Linux or macOS, activate the environment with `source .venv/bin/activate` instead of the PowerShell activation command.

## Quick Start

Replace the example URL or selections with the MangaFire resource you want to download.

### Download a direct volume or chapter URL

A direct volume or chapter URL can be passed on its own:

```powershell
mangafire-dl "https://mangafire.to/title/027-bleach/volume/144857"
```

```powershell
mangafire-dl "https://mangafire.to/title/027-bleach/chapter/6056551"
```

Direct resource URLs must not be combined with `--lang`, `--volumes`, or `--chapters`.

### Download selected volumes from a manga page

```powershell
mangafire-dl "https://mangafire.to/title/027-bleach" --lang pt-br --volumes "1-5"
```

### Download selected chapters from a manga page

```powershell
mangafire-dl "https://mangafire.to/title/027-bleach" --lang en --chapters "1-5, 10, 12-15"
```

### Choose an output directory

Add `--output` to any supported command:

```powershell
mangafire-dl "https://mangafire.to/title/027-bleach" --lang pt-br --volumes "1-5" --output "D:\Mangas"
```

By default, downloaded files are saved in the operating system's Downloads directory.

## Usage

### Command-line syntax

```text
mangafire-dl URL [--lang LANGUAGE] [--volumes SELECTION | --chapters SELECTION] [--output PATH]
```

### Options

| Option | Description |
| --- | --- |
| `URL` | MangaFire manga page, volume URL, or chapter URL. Required. |
| `--lang LANGUAGE` | Language code for resources selected from a manga page. Required for manga-page downloads. Examples: `pt-br`, `en`. |
| `--volumes SELECTION` | Volumes to download from a manga page. Mutually exclusive with `--chapters`. |
| `--chapters SELECTION` | Chapters to download from a manga page. Mutually exclusive with `--volumes`. |
| `--output PATH` | Output directory. Defaults to the operating system's Downloads directory. |
| `--help` | Show command-line help. |
| `--version` | Show the installed version. |

For a manga-page URL, provide `--lang` and exactly one of `--volumes` or `--chapters`. For a direct volume or chapter URL, provide only the URL and, optionally, `--output`.

### Selection syntax

Selections accept individual numbers, ranges, and comma-separated combinations:

```text
1
1-5
1, 6, 12
1-5, 8, 12-15
```

Use quotes around a selection in shell commands, especially when it contains commas or spaces.

## Output Structure

Downloads are organized by manga and resource type. For example:

```text
Downloads/
└── Bleach/
    ├── volumes/
    │   ├── Bleach - Volume 01.cbz
    │   └── Bleach - Volume 02.cbz
    └── chapters/
        ├── Bleach - Chapter 001.cbz
        └── Bleach - Chapter 002.cbz
```

Volume numbers are normally padded to two digits and chapter numbers to three digits. Decimal chapter numbers retain their decimal part. The manga folder and filenames are derived from the resource's title.

## Requirements

- **Python package:** Python 3.10 or newer.
- **Runtime dependencies:** `gallery-dl` and `requests` are declared by the package and installed automatically by `pip` or `pipx`.
- **Windows portable ZIP:** does not require a separate Python or `gallery-dl` installation. Keep the EXE and its `_internal` directory together.

## Troubleshooting

- **The terminal closes after double-clicking the EXE:** the EXE is a command-line application and expects a URL argument. Use `Executar.bat` for an interactive prompt, or launch `mangafire-dl.exe` from an already-open terminal with the URL and options.
- **A manga-page URL is rejected:** include `--lang` and either `--volumes` or `--chapters`.
- **A direct volume or chapter URL is rejected when options are supplied:** direct resource URLs cannot be combined with `--lang`, `--volumes`, or `--chapters`.
- **No resources are found:** check the selected language and the volume/chapter numbers available on MangaFire.
- **A request fails:** check your internet connection and whether MangaFire is reachable, then retry. Site responses and available resources can change.
- **The portable build fails to start:** extract the complete ZIP and keep `mangafire-dl.exe`, `Executar.bat`, and `_internal` in the same folder.

## Limitations

- The tool depends on MangaFire's current site behavior and the resources available there; changes to the site may require updates.
- The command-line interface does not currently provide a graphical user interface.
- The Windows portable build is distributed as a folder packaged in a ZIP, not as a Windows installer.

## For Developers

### Development setup

Clone the repository and create a virtual environment:

```powershell
git clone https://github.com/Osanticide/mangafire-dl.git
cd mangafire-dl
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

On Linux, activate the environment with `source .venv/bin/activate`.

### Run tests

```powershell
python -m pytest
```

### Build release artifacts

```powershell
python scripts/build_release.py
```

The build script runs the test suite and builds the Python wheel and source distribution. When run on Windows, it also builds the Windows standalone folder and creates the portable ZIP. Run the script on each target operating system; PyInstaller does not cross-build a Windows executable from Linux or a Linux executable from Windows.

Build outputs are written to `dist/`. The script prepares artifacts locally; it does not publish them to PyPI or create a GitHub Release automatically.

## Contributing

Bug reports, suggestions, and pull requests are welcome. Before opening a pull request, run the test suite and describe the behavior your change affects.

## License

The original MangaFire Downloader project is licensed under the [MIT License](LICENSE). Third-party components, including [`gallery-dl`](https://github.com/mikf/gallery-dl), remain subject to their respective licenses.

## Acknowledgements

MangaFire Downloader uses [`gallery-dl`](https://github.com/mikf/gallery-dl) as the underlying download component. Many thanks to its developers and contributors for creating and maintaining that project.

## Disclaimer

MangaFire Downloader is an independent third-party project and is not affiliated with, endorsed by, or maintained by MangaFire or the `gallery-dl` project. Users are responsible for complying with applicable laws, copyright requirements, and the terms that apply to the websites and content they access.