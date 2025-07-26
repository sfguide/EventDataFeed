from flask import Flask, jsonify
from flask_cors import CORS
import requests, os

app = Flask(__name__)
CORS(app)

EVENTBRITE_TOKEN = os.environ.get('EVENTBRITE_TOKEN')
ORGANIZER_ID = os.environ.get('EVENTBRITE_ORG_ID')

@app.route("/test")
def test():
    return jsonify({"message": "This is the /test route."})

@app.route("/")
def home():
    return "Eventbrite Proxy is running!"

@app.route("/debug")
def debug():
    return "Debug route: this proxy app is active."

@app.route("/events")
def get_events():
    print(">>> /events route was hit")
    if not EVENTBRITE_TOKEN:
        print(">>> Missing EVENTBRITE_TOKEN")
        return jsonify({"error": "Missing EVENTBRITE_TOKEN"}), 500

    headers = {"Authorization": f"Bearer {EVENTBRITE_TOKEN}"}
    params = {"expand": "venue"}

    if ORGANIZER_ID:
        params["organizer.id"] = ORGANIZER_ID

    try:
        response = requests.get("https://www.eventbriteapi.com/v3/events/search/", headers=headers, params=params)
        print(">>> Eventbrite API call status:", response.status_code)
        if response.ok:
            return jsonify(response.json())
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        print(">>> Exception:", e)
        return jsonify({"error": str(e)}), 500
