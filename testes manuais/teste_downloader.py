from mangafire.downloader import GalleryDLDownloader


def main() -> None:
    downloader = GalleryDLDownloader()

    downloader.download("https://mangafire.to/title/027-bleach/volume/144857")

    print("Download concluído com sucesso.")


if __name__ == "__main__":
    main()
