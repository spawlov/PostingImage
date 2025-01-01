import argparse
import os
from argparse import ArgumentParser
from random import randint
from time import sleep
from urllib.parse import urlparse

from dotenv import find_dotenv, load_dotenv

import telegram


def create_parser() -> ArgumentParser:
    parser = argparse.ArgumentParser(description="Публикация фотографий в телеграм канал")
    parser.add_argument(
        "-photo",
        "--photo_path",
        default=None,
        help="путь к файлу или url с фотографией для публикации",
    )
    parser.add_argument(
        "-period",
        "--posting_period",
        default=None,
        help="периодичность публикации случайно выбранной фотографии",
    )
    return parser


def is_url(path):
    parsed = urlparse(path)
    return parsed.scheme in ("http", "https", "ftp", "ftps")


def main() -> None:
    load_dotenv(find_dotenv())
    tg_token = os.environ["TG_BOT_TOKEN"]
    chanel_id = os.environ["TG_CHANEL_ID"]
    posting_period = os.environ["TG_POSTING_PERIOD"]

    bot = telegram.Bot(tg_token)

    parser = create_parser()
    namespace = parser.parse_args()

    if namespace.photo_path:
        if is_url(namespace.photo_path):
            bot.send_photo(chat_id=chanel_id, photo=namespace.photo_path)
            return
        bot.send_photo(chat_id=chanel_id, photo=open(namespace.photo_path, "rb"))
        return

    if namespace.posting_period:
        posting_period = namespace.posting_period

    images = []
    for root, _, files in os.walk("images"):
        for name in files:
            images.append(f"{root}/{name}")

    while True:
        image_no = randint(0, len(images))
        bot.send_photo(chat_id=chanel_id, photo=open(images[image_no], "rb"))
        sleep(int(posting_period))


if __name__ == "__main__":
    main()
