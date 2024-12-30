import argparse
from argparse import ArgumentParser

from handlers import download_image, get_file_extension, get_md5_timestamp

import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/39.0.2171.95 Safari/537.36",
}


def create_parser() -> ArgumentParser:
    parser = argparse.ArgumentParser(description="Загрузка фотографий сделанных на пусках SPACEX")
    parser.add_argument(
        "-id",
        "--id_launch",
        default="latest",
        help="id пуска (all - загрузка фотографий со всех пусков, начиная с последнего)",
    )
    parser.add_argument(
        "-l",
        "--limit",
        default=None,
        help="лимит загружаемых фотографий (количество пусков для загрузки) - только если id=all",
    )
    return parser


def fetch_spacex_launch(launch_id: str) -> None:
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    with requests.get(url=url, headers=HEADERS, timeout=30) as response:
        response.raise_for_status()
        spacex_links = response.json()["links"]["flickr"]["original"]

    print(f"Скачивается {len(spacex_links)} фотографий пуска №{response.json()["flight_number"]}")  # noqa

    for link in spacex_links:
        download_image(
            url=link.strip(),
            path="images/spacex_temp",
            filename=f"{get_md5_timestamp(8)}{get_file_extension(link.strip())}",
        )


def fetch_spacex_all_launch(limit: int | None = None):
    url = "https://api.spacexdata.com/v5/launches"
    with requests.get(url=url, headers=HEADERS, timeout=30) as response:
        response.raise_for_status()

    indexes = []
    count_photos = 0
    for launch in reversed(response.json()):
        if launch["links"]["flickr"]["original"]:
            indexes.append(launch["id"])
            count_photos += len(launch["links"]["flickr"]["original"])

    for index in indexes[:limit]:
        fetch_spacex_launch(index)


def main():
    parser = create_parser()
    namespace = parser.parse_args()
    if namespace.id_launch == "all":
        fetch_spacex_all_launch(int(namespace.limit))
    else:
        fetch_spacex_launch(namespace.id_launch)


if __name__ == "__main__":
    main()
