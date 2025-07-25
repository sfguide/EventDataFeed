from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

EVENTBRITE_TOKEN = os.environ.get('EVENTBRITE_TOKEN')
ORGANIZER_ID = os.environ.get('EVENTBRITE_ORG_ID')  # Optional

@app.route("/")
def home():
    return "Eventbrite Proxy is running!"

@app.route("/events")
def get_events():
    if not EVENTBRITE_TOKEN:
        return jsonify({"error": "Missing EVENTBRITE_TOKEN"}), 500

    headers = {
        "Authorization": f"Bearer {EVENTBRITE_TOKEN}"
    }

    base_url = "https://www.eventbriteapi.com/v3/events/search/"
    params = {"expand": "venue"}

    if ORGANIZER_ID:
        params["organizer.id"] = ORGANIZER_ID

    response = requests.get(base_url, headers=headers, params=params)
    if response.ok:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.text}), response.status_code
