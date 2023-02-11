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

    elif request.method == 'HEAD':
        send_main()


def sender():
    

app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
