import sys
sys.path.append("..")  # To import detector.py from parent directory

from flask import Flask, request, jsonify, render_template
from detector import detect_people
import cv2
import numpy as np
import requests

TELEGRAM_BOT_TOKEN = '7862349383:AAHjvBLGj9VNtqZvlkdYj1D0UNoKT132LIw'
TELEGRAM_CHAT_ID = '5527189799'
CROWD_LIMIT = 5

app = Flask(__name__, template_folder="../templates")

def send_telegram_alert(count, frame):
    message = (
        "🚔 Patrol Alert\n"
        f"👥 Crowd size: {count}\n"
        "🚨 Situation requires attention.\n"
        "📡 Surveillance feed active."
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    _, img_encoded = cv2.imencode('.jpg', frame)
    files = {'photo': ('image.jpg', img_encoded.tobytes())}
    data = {"chat_id": TELEGRAM_CHAT_ID, "caption": message}
    try:
        requests.post(url, data=data, files=files, timeout=5)
    except Exception:
        pass

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/detect", methods=["POST"])
def detect():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    npimg = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    frame, count = detect_people(frame)
    if count > CROWD_LIMIT:
        send_telegram_alert(count, frame)
    return jsonify({"count": count})

# Vercel expects the variable to be named 'app'
handler = app
