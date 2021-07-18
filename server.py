import json
import os
import requests
from requests_html import HTML

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

def url_to_text(url):
    r = requests.get(url)
    if r.status_code == 200:
        html_text = r.text
        return html_text
    
# It will parse the html data into structure way 
def pharse_and_extract(url):
  # it will get the html data from url
    html_text = url_to_text(url)
    if html_text is None:
        return ""
    r_html = HTML(html=html_text)
    return r_html
  
def extract_from_css_tricks(res_html):
    resulted_tricks = []
    titles=res_html.find(".article-article h2 a")
    for title in titles:
      resulted_tricks.append(title.attrs['href'])
    return resulted_tricks

def extract_icons_url(res_html,limit=1):
    icons_url = []
    titles=res_html.find(".icon--holder>a>img")
    for title in titles:
      icons_url.append(title.attrs['data-src'])
    return " \n".join(icons_url[:limit])

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
    elif message.startswith('/icon'):
        search_icon,*params = message.split(" ")
        if len(params)>1:
            flaticon_url = f"https://www.flaticon.com/search?word={params[0]}"
            icons = extract_icons_url(pharse_and_extract(flaticon_url),limit=int(params[-1]))
            reply = icons
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
