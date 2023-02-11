import os
import json
from flask import Flask, request, Response
import telebot
bot = telebot.TeleBot(os.environ.get("TOKEN"))
app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle():
    if request.form.get("mypas") != None:
        sender(request.form.get("mypas"))

        

def sender(obj):
    bot.send_photo(os.environ.get("DIR"), obj['link'], caption=obj['text'], parse_mode="Markdown")
    

app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
