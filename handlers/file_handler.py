import hashlib
import os
from time import time
from typing import Union
from urllib.parse import urlparse

import requests

from tqdm import tqdm

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/39.0.2171.95 Safari/537.36",
}


def make_dir(path: str) -> str:
    path = os.path.normpath(f"{os.getcwd()}/{path.strip()}")
    os.makedirs(path, exist_ok=True)
    return path


def get_md5_timestamp(length: int = 32) -> str:
    return hashlib.md5(str(time()).encode("utf-8")).hexdigest()[:length]


def get_file_extension(url: str) -> str:
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = os.path.basename(path)
    _, extension = os.path.splitext(filename)
    return extension.lower()


def download_image(url: str, path: str, filename: str, api_key: Union[str, None] = None) -> None:
    params = None
    if api_key:
        params = {
            "api_key": api_key,
        }
    response = requests.get(url=url, headers=HEADERS, params=params, stream=True, timeout=30)
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
