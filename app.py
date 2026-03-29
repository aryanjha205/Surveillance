from flask import Flask, render_template, Response
import cv2
from detector import detect_people
import requests
from datetime import datetime
import os
import json

app = Flask(__name__)
cap = cv2.VideoCapture(0)  # Use 0 for webcam, or IP cam URL

CROWD_LIMIT = 5

# Telegram Bot configuration (replace with your actual bot token and chat id)
TELEGRAM_BOT_TOKEN = '7862349383:AAHjvBLGj9VNtqZvlkdYj1D0UNoKT132LIw'
TELEGRAM_CHAT_ID = '5527189799'

alert_sent = False  # To avoid spamming messages

CHAT_IDS_FILE = "chat_ids.json"

def add_chat_id(chat_id):
    chat_ids = []
    if os.path.exists(CHAT_IDS_FILE):
        with open(CHAT_IDS_FILE, "r") as f:
            chat_ids = json.load(f)
    # Ensure chat_id is string for consistency
    chat_id = str(chat_id)
    if chat_id not in chat_ids:
        chat_ids.append(chat_id)
        with open(CHAT_IDS_FILE, "w") as f:
            json.dump(chat_ids, f)

# Add chat IDs manually here
add_chat_id("5527189799")      # Example: your own chat ID
add_chat_id("5176674442")      # Example: Rachit Parikh's chat ID
# Add more chat IDs as needed:
# add_chat_id("another_chat_id")

def get_all_chat_ids():
    if os.path.exists(CHAT_IDS_FILE):
        with open(CHAT_IDS_FILE, "r") as f:
            return json.load(f)
    return []

def send_telegram_alert(count, frame):
    global alert_sent
    if not alert_sent:
        now = datetime.now()
        date_str = "🗓️ " + now.strftime("%Y-%m-%d")
        time_str = "🕒 " + now.strftime("%H:%M:%S")
        message = (
            "🚔 Patrol Alert\n"
            f"👥 Crowd size: {count}\n"
            "🚨 Situation requires attention.\n"
            "📡 Surveillance feed active.\n"
            f"{date_str}\n"
            f"{time_str}\n"
        )
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        _, img_encoded = cv2.imencode('.jpg', frame)
        files = {'photo': ('image.jpg', img_encoded.tobytes())}
        chat_ids = get_all_chat_ids()
        # Ensure at least the manually added chat IDs are present
        if not chat_ids:
            chat_ids = ["5527189799", "5176674442"]  # fallback to manual list
        for chat_id in chat_ids:
            try:
                data = {"chat_id": int(chat_id), "caption": message}
                response = requests.post(url, data=data, files=files, timeout=10)
                print(f"Telegram response for chat_id {chat_id}: {response.status_code} {response.text}")
            except Exception as e:
                print(f"Error sending to chat_id {chat_id}: {e}")
        alert_sent = True

def gen_frames():
    global alert_sent
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame, count = detect_people(frame)
        # Show the current count on the frame
        cv2.putText(frame, f"Count: {count}", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        if count > CROWD_LIMIT:
            cv2.putText(frame, "ALERT: Crowd Limit Exceeded!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        if count > 2:
            send_telegram_alert(count, frame)
        else:
            alert_sent = False  # Reset if count drops below threshold
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
