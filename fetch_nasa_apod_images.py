import os
from typing import Any

from dotenv import find_dotenv, load_dotenv

from handlers import download_image, get_file_extension, get_md5_timestamp

import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/39.0.2171.95 Safari/537.36",
}


def fetch_nasa_apod_images(api_key: str, file_params: dict[str, str], count: int) -> None:
    url = "https://api.nasa.gov/planetary/apod"
    params: dict[str, Any] = {
        "count": count,
        "api_key": api_key,
    }
    with requests.get(url=url, headers=HEADERS, params=params, timeout=30) as response:
        response.raise_for_status()
        nasa_links = [item["hdurl"].strip() for item in response.json()]

    for i, link in enumerate(nasa_links):
        filename = f"{file_params['filename']}_{i}"
        if filename.startswith("random"):
            filename = get_md5_timestamp(8)
        download_image(
            url=link,
            api_key=api_key,
            path=file_params["path"],
            filename=f"{filename}{get_file_extension(link)}",
        )


def main():
    load_dotenv(find_dotenv())
    api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
    file_params = {
        "path": os.getenv("NASA_APOD_PATH", "images"),
        "filename": os.getenv("NASA_APOD_FILENAME", "random"),
    }
    count = int(os.getenv("NASA_APOD_COUNT", 50))
    try:
        fetch_nasa_apod_images(api_key, file_params, count)
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.HTTPError,
        KeyError,
        ValueError,
    ) as error:
        print(str(error))  # noqa


if __name__ == "__main__":
    main()
