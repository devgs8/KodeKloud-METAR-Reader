import re

import requests
from flask import Flask, render_template, request

from decoder import decode

API_URL = "https://aviationweather.gov/api/data/metar"
app = Flask(__name__)


def fetch_metar(code):
    resp = requests.get(API_URL, params={"ids": code, "format": "json"}, timeout=10,
                        headers={"User-Agent": "metar-reader-flask"})
    resp.raise_for_status()
    if resp.status_code == 204 or not resp.text.strip():
        return None
    data = resp.json()
    return data[0] if data else None


@app.route("/")
def index():
    code = (request.args.get("code") or "").strip().upper()
    report = error = None
    if code:
        if not re.fullmatch(r"[A-Z0-9]{3,4}", code):
            error = "Please enter a 3-4 character airport code, like KHIO."
        else:
            try:
                metar = fetch_metar(code)
                # US users often type 3-letter FAA codes (e.g. HIO); retry as ICAO.
                if metar is None and len(code) == 3:
                    metar = fetch_metar("K" + code)
                if metar is None:
                    error = f"No current weather report found for '{code}'."
                else:
                    report = decode(metar)
            except (requests.RequestException, ValueError):
                error = "Couldn't reach the weather service. Please try again."
    return render_template("index.html", code=code, report=report, error=error)


if __name__ == "__main__":
    app.run(debug=True)
