import os

from dotenv import find_dotenv, load_dotenv

from handlers import download_image, get_file_extension, get_md5_timestamp

import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/39.0.2171.95 Safari/537.36",
}


def fetch_nasa_epic_images(api_key: str, file_params: dict[str, str]) -> None:
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
        "path": os.getenv("NASA_EPIC_PATH", "images"),
        "filename": os.getenv("NASA_EPIC_FILENAME", "random"),
    }
    try:
        fetch_nasa_epic_images(api_key, file_params)
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
