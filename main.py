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
    if not EVENTBRITE_TOKEN:
        return jsonify({"error": "Missing EVENTBRITE_TOKEN"}), 500
    headers = {"Authorization": f"Bearer {EVENTBRITE_TOKEN}"}
    params = {"expand": "venue"}
    if ORGANIZER_ID:
        params["organizer.id"] = ORGANIZER_ID
    resp = requests.get("https://www.eventbriteapi.com/v3/events/search/", headers=headers, params=params)
    if resp.ok:
        return jsonify(resp.json())
    return jsonify({"error": resp.text}), resp.status_code
