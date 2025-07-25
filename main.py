from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

EVENTBRITE_TOKEN = os.environ.get('EVENTBRITE_TOKEN')
ORGANIZER_ID = os.environ.get('EVENTBRITE_ORG_ID')  # Optional

@app.route("/events")
def get_events():
    headers = {
        "Authorization": f"Bearer {EVENTBRITE_TOKEN}"
    }

    # Optional: fetch only events from a specific organizer
    base_url = "https://www.eventbriteapi.com/v3/events/search/"
    params = {
        "organizer.id": ORGANIZER_ID,
        "expand": "venue"
    }

    response = requests.get(base_url, headers=headers, params=params)
    if response.ok:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.text}), response.status_code

@app.route("/")
def home():
    return "Eventbrite Proxy is running!"
