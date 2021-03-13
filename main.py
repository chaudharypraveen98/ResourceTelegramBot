import json

import requests

Token = "Enter Your Token"


class ResourceBot():
    def __init__(self):
        self.token = Token
        self.base = f"https://api.telegram.org/bot{self.token}"

    def get_updates(self, offset=None):
        url = f"{self.base}/getUpdates?timeout=100"
        if offset:
            url = url + f"&offset={offset + 1}"
        r = requests.get(url)
        return json.loads(r.content)

    def send_messages(self, msg, chat_id):
        url = f"{self.base}/sendMessage?chat_id={chat_id}&text={msg}"
        if msg is not None:
            requests.get(url) 
