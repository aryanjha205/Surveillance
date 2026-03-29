# 👁️‍🗨️ Crowd Counter with Telegram Alert 🚨

This project uses OpenCV, YOLOv8, and Flask to count people in real-time from a webcam or IP camera feed. When the crowd count exceeds a set threshold, it sends an alert to Telegram using the bot [@CrowdEye_bot](https://t.me/CrowdEye_bot), including a photo of the current scene.

## ✨ Features

- 👤 Real-time people detection and counting using YOLOv8
- 🖥️ Web dashboard for live video and stats
- 🚨 Telegram alert with photo when crowd exceeds threshold (uses [@CrowdEye_bot](https://t.me/CrowdEye_bot))
- 🔧 Easily configurable for webcam or IP camera

## ⚙️ How It Works

1. 📷 The app captures video frames and detects people using YOLOv8.
2. 📊 The current count is displayed on the web dashboard.
3. 🚨 If the count exceeds the threshold (default: 2), a Telegram alert is sent via [@CrowdEye_bot](https://t.me/CrowdEye_bot) **with a photo of the current frame**.

## 🛠️ Setup

1. **Clone this repository and install dependencies:**
   ```
   pip install ultralytics opencv-python flask requests numpy
   ```

2. **Download the YOLOv8 model:**
   ```python
   from ultralytics import YOLO
   model = YOLO("yolov8n.pt")
   ```


3. **Run the app:**
   ```
   python app.py
   ```
   🌐 Open your browser at `http://127.0.0.1:5000/` to view the dashboard.

## 📝 How to Register for Telegram Alerts

1. **Start a chat with the bot:**
   - Open Telegram and search for [@CrowdEye_bot](https://t.me/CrowdEye_bot).
   - Click "Start" or send any message to the bot.

2. **Get your chat ID:**
   - After sending a message to the bot, open this link in your browser:
     ```
     https://api.telegram.org/bot7862349383:AAHjvBLGj9VNtqZvlkdYj1D0UNoKT132LIw/getUpdates
     ```
   - Look for `"chat":{"id":...}` in the JSON response. The number after `"id":` is your chat ID.

3. **Register your chat ID:**
   - Use a tool like `curl`, Postman, or Python to send a POST request to the Flask app:
     ```bash
     curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d "{\"chat_id\": \"YOUR_CHAT_ID\"}"
     ```
     Or with Python:
     ```python
     import requests
     requests.post("http://localhost:5000/register", json={"chat_id": "YOUR_CHAT_ID"})
     ```
   - Replace `YOUR_CHAT_ID` with the number you found in step 2.

4. **Done!**
   - You will now receive Telegram alerts when the crowd count exceeds the threshold.

## 🙏 Credits

- 🦾 YOLOv8 by Ultralytics
- 🧑‍💻 Flask
- 🎥 OpenCV
- 📲 Telegram Bot API ([CrowdEye_bot](https://t.me/CrowdEye_bot))
