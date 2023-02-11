import os
import json
from flask import Flask, request, Response
import telebot

now_utc = [datetime.now().utcnow(), "No date"]
results_main = []
bot = telebot.TeleBot(os.environ.get("TOKEN"))
app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle():
    if request.form.get("mypas") == 'pass':
        

    elif request.method == 'HEAD':
        send_main()


def send_main():
    for i in range(3):
        try:
            if len(results_main) != 0:
                image = results_main.pop()
                bot.send_photo(
                    chat_id="@mjrecent_f",
                    photo=image["link"],
                    caption=image["prompt"],
                    parse_mode="Markdown"
                )
            else:
                bot.send_message(os.environ.get("LOGS_USERNAME"), "No images, called get_main(now_utc)")
                get_main(now_utc)
                continue

            break
        except Exception as e:
            e = str(e)
            bot.send_message(os.environ.get("LOGS_USERNAME"), f"error:\n{e}")
            if "Bad Request" in e:
                continue
            else:
                break
                
    bot.send_message(os.environ.get("LOGS_USERNAME"), f"{len(results_main)} pictures left.")


app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
