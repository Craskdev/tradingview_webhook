﻿from flask import Flask, request, jsonify
import json
import requests

# Load Telegram credentials
with open("credentials.json") as f:
    creds = json.load(f)

TELEGRAM_TOKEN = creds["telegram_token"]
CHAT_ID = creds["telegram_chat_id"]

app = Flask(__name__)

# Store the latest signal here
latest_signal = {"message": None}

def send_to_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, json=payload)
    return response.ok, response.text

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("⚠️ Raw payload:", data, flush=True)

    message = data.get("alert") or data.get("message") or json.dumps(data)
    if not message:
        return jsonify({"error": "Missing 'alert' or 'message' field"}), 400

    latest_signal["message"] = message  # 🟢 Save latest alert message

    print(f"Received TradingView message: {message}")
    success, resp = send_to_telegram(message)
    if success:
        return jsonify({"status": "Sent to Telegram"}), 200
    else:
        return jsonify({"error": f"Telegram failed: {resp}"}), 500

# New endpoint for polling latest alert
@app.route("/last-signal", methods=["GET"])
def last_signal():
    return jsonify(latest_signal)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
