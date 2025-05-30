from flask import Flask, request, jsonify
import json
import requests

# Load Telegram credentials
with open("credentials.json") as f:
    creds = json.load(f)

TELEGRAM_TOKEN = creds["telegram_token"]
CHAT_ID = creds["telegram_chat_id"]

app = Flask(__name__)

def send_to_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, json=payload)
    return response.ok, response.text

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("⚠️ Raw payload:", data)  # 👈 this line is critical



    if not message:
        return jsonify({"error": "Missing 'alert' or 'message' field"}), 400

    print(f"Received TradingView message: {message}")
    success, resp = send_to_telegram(message)
    if success:
        return jsonify({"status": "Sent to Telegram"}), 200
    else:
        return jsonify({"error": f"Telegram failed: {resp}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
