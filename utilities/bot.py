import os

import requests


def send_message(text):
    token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    url = (
        f"https://api.telegram.org/bot{token}/"
        f"sendMessage?chat_id={chat_id}&text={text}"
    )
    requests.post(url)
