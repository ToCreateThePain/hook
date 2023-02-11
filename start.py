import os
import json
from datetime import datetime
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


def get_main(prev_utc):
    bot.send_message(os.environ.get("LOGS_USERNAME"), f"Before get_main time is\n{str(prev_utc)}")
    results_main.clear()
    response = requests.get("https://www.midjourney.com/showcase/recent/")
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all("script")
    for script in scripts:
        if script.get('id') != None:
            data = json.loads(script.text)
            jobs = data['props']['pageProps']['jobs']
            if prev_utc[1] == "No date":
                now_utc[1] = "Set date"
                for job in jobs:
                    results_main.append({"link": job['image_paths'][0],
                                         "prompt": f"`{job['full_command']}`"
                                         })
            else:
                for job in jobs:
                    day_job = int(job['enqueue_time'][8:10])
                    hour_job = int(job['enqueue_time'][11:13])
                    min_job = int(job['enqueue_time'][14:16])
                    if prev_utc[0].day <= day_job and prev_utc[0].hour <= hour_job and prev_utc[0].minute <= min_job:
                        results_main.append({"link": job['image_paths'][0],
                                             "prompt": f"`{job['full_command']}`"
                                             })

            break

    now_utc[0] = datetime.now().utcnow()
    bot.send_message(os.environ.get("LOGS_USERNAME"), f"Got {len(results_main)} new images!\n{now_utc[1]} {str(now_utc[0])}")


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
