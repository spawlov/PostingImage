import os

from dotenv import find_dotenv, load_dotenv

import telegram


def main() -> None:
    load_dotenv(find_dotenv())
    tg_token = os.environ["TG_BOT_TOKEN"]
    chanel_id = os.environ["TG_CHANEL_ID"]

    bot = telegram.Bot(tg_token)
    # bot.send_message(chat_id=chanel_id, text="Test message for chanel.")
    bot.send_photo(chat_id=chanel_id, photo=open("images/spacex/spacex_13_0.jpg", "rb"))


if __name__ == "__main__":
    main()
