import hashlib
import os
from time import time
from typing import Any
from urllib.parse import urlparse

from dotenv import find_dotenv, load_dotenv

import requests

from tqdm import tqdm

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/39.0.2171.95 Safari/537.36",
}


def make_dir(path: str) -> str:
    path = os.path.normpath(f"{os.getcwd()}/{path.strip()}")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_md5_timestamp(length: int = 32) -> str:
    return hashlib.md5(str(time()).encode("utf-8")).hexdigest()[:length]


def get_file_extension(url: str) -> str:
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = os.path.basename(path)
    _, extension = os.path.splitext(filename)
    return extension.lower()


def download_image(url: str, api_key: str, path: str, filename: str) -> None:
    params = {
        "api_key": api_key,
    }
    with requests.get(url=url, headers=HEADERS, params=params, stream=True, timeout=30) as response:
        response.raise_for_status()

        total_length = response.headers.get("Content-Length")
        if not total_length:
            raise ValueError("Content-Length is None")

        filename = f"{make_dir(path)}/{filename}"
        with open(filename, "wb") as file:
            with tqdm(
                total=int(total_length),
                unit="B",
                unit_scale=True,
                colour="green",
                desc=filename,
            ) as progress_bar:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
                    progress_bar.update(len(chunk))


def fetch_spacex_last_launch(api_key: str) -> None:
    url = "https://api.spacexdata.com/v5/launches/61eefaa89eb1064137a1bd73"
    with requests.get(url=url, headers=HEADERS, timeout=30) as response:
        response.raise_for_status()
        spacex_links = response.json()["links"]["flickr"]["original"]

    for i, link in enumerate(spacex_links):
        download_image(
            url=link.strip(),
            api_key=api_key,
            path="images/spacex",
            filename=f"image_{i}{get_file_extension(link.strip())}",
        )


def fetch_nasa_apod_images(api_key: str, count: int = 50) -> None:
    url = "https://api.nasa.gov/planetary/apod"
    params: dict[str, Any] = {
        "count": count,
        "api_key": api_key,
    }
    with requests.get(url=url, headers=HEADERS, params=params, timeout=30) as response:
        response.raise_for_status()
        nasa_links = [item["hdurl"].strip() for item in response.json()]

    for i, link in enumerate(nasa_links):
        download_image(
            url=link,
            api_key=api_key,
            path="images/apod_nasa",
            filename=f"image_{i}{get_file_extension(link)}",
        )


def fetch_nasa_epic_images(api_key: str) -> None:
    url = "https://api.nasa.gov/EPIC/api/natural"
    params = {
        "api_key": api_key,
    }
    epic_links = []
    with requests.get(url=url, headers=HEADERS, params=params, timeout=30) as response:
        response.raise_for_status()
        for item in response.json():
            date = item["date"].split()[0].replace("-", "/")
            filename = item["image"]
            epic_links.append(f"https://api.nasa.gov/EPIC/archive/natural/{date}/png/{filename}.png")

    for i, link in enumerate(epic_links):
        download_image(
            url=link,
            api_key=api_key,
            path="images/epic_nasa",
            filename=f"image_{i}{get_file_extension(link)}",
        )


def main() -> None:
    load_dotenv(find_dotenv())
    api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
    fetch_spacex_last_launch(api_key)
    fetch_nasa_apod_images(api_key)
    fetch_nasa_epic_images(api_key)


if __name__ == "__main__":
    main()
