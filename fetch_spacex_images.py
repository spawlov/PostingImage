import argparse
import os
from argparse import ArgumentParser
from typing import Dict, Union

from dotenv import find_dotenv, load_dotenv

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
        "-no",
        "--launch_no",
        default="latest",
        help="номер пуска (all - загрузка фотографий со всех пусков, начиная с последнего)",
    )
    parser.add_argument(
        "-l",
        "--limit",
        default=None,
        help="лимит загружаемых фотографий (количество пусков для загрузки) - только если id=all",
    )
    return parser


def get_id_launch_at_number(launch_no: str) -> Union[str, None]:
    if not launch_no.isdigit():
        return launch_no

    url = "https://api.spacexdata.com/v5/launches"
    response = requests.get(url=url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    for launch in response.json():
        if int(launch_no) == launch["flight_number"]:
            return launch["id"]
    return None


def fetch_spacex_launch(file_params: Dict[str, str], launch_no: str) -> None:
    url = f"https://api.spacexdata.com/v5/launches/{get_id_launch_at_number(launch_no)}"
    response = requests.get(url=url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    spacex_links = response.json()["links"]["flickr"]["original"]

    print(f"Скачивается {len(spacex_links)} фотографий пуска №{response.json()['flight_number']}")  # noqa

    for index, link in enumerate(spacex_links):
        filename = f"{file_params['filename']}_{response.json()['flight_number']}_{index}"
        if filename.startswith("random"):
            filename = get_md5_timestamp(8)
        download_image(
            url=link.strip(),
            path=file_params["path"],
            filename=f"{filename}{get_file_extension(link.strip())}",
        )


def fetch_spacex_all_launches(file_params: Dict[str, str], limit: Union[int, None] = None):
    url = "https://api.spacexdata.com/v5/launches"
    response = requests.get(url=url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    launch_ids = []
    for launch in reversed(response.json()):
        if launch["links"]["flickr"]["original"]:
            launch_ids.append(launch["id"])

    for launch_id in launch_ids[:limit]:
        fetch_spacex_launch(file_params, launch_id)


def main():
    load_dotenv(find_dotenv())
    file_params = {
        "path": os.getenv("SPACEX_PATH", "images"),
        "filename": os.getenv("SPACEX_FILENAME", "random"),
    }

    parser = create_parser()
    namespace = parser.parse_args()

    if namespace.launch_no == "all":
        fetch_spacex_all_launches(file_params, int(namespace.limit))
    else:
        fetch_spacex_launch(file_params, namespace.launch_no)


if __name__ == "__main__":
    main()
