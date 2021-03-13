import json
import os
import random

from main import ResourceBot

update_id = None

Bot = ResourceBot()

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(f'{dir_path}/memes.json', encoding="utf8") as file:
    meme_data = json.loads(file.read())

with open(f'{dir_path}/quotes.json', encoding="utf8") as file:
    quotes_data = json.loads(file.read())


def format_message(msg):
    formatted_msg = ""
    for i in msg:
        formatted_msg += f"{i.upper()} ---> {msg[i]}\n"
    return formatted_msg


def make_reply(message):
    reply = None
    if message == '/help':
        reply = "Type \n/meme to get meme \n/quote to get quote"
    elif message == '/meme':
        reply = random.choice(meme_data)
    elif message == '/resource':
        reply = "https://css-tricks.com/too-many-svgs-clogging-up-your-markup-try-use/"
    elif message == '/quote':
        reply = format_message(random.choice(quotes_data))
    return reply


while True:
    print("....")
    updates = Bot.get_updates(offset=update_id)
    updates = updates['result']
    if updates:
        for item in updates:
            update_id = item['update_id']
            try:
                message = item["message"]["text"]
            except:
                message = None
            from_ = item['message']['from']['id']
            reply = make_reply(message)
            Bot.send_messages(reply, from_)
