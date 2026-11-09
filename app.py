"""METAR Reader: a small Flask app that explains airport weather in plain English.

The user enters an airport code. The app fetches the latest METAR (a
standardized, cryptic aviation weather report) from aviationweather.gov and
uses :mod:`decoder` to turn it into a friendly, readable summary.

Run locally with ``python app.py`` and open http://127.0.0.1:5000.
"""

import re

import requests
from flask import Flask, render_template, request

from decoder import decode

# Public NOAA Aviation Weather Center endpoint; no API key required.
API_URL = "https://aviationweather.gov/api/data/metar"
REQUEST_TIMEOUT_SECONDS = 10

# Airport identifiers are 3 characters (FAA, e.g. "HIO") or 4 (ICAO, e.g. "KHIO").
AIRPORT_CODE_PATTERN = re.compile(r"[A-Z0-9]{3,4}")

app = Flask(__name__)


def fetch_metar(code):
    """Fetch the most recent METAR for an airport.

    Args:
        code: An uppercase airport identifier, such as ``"KHIO"``.

    Returns:
        The METAR record as a dict (as returned by the API's JSON format), or
        ``None`` if the API has no report for that identifier.

    Raises:
        requests.RequestException: If the request fails or the API returns an
            HTTP error status.
        ValueError: If the API response body is not valid JSON.
    """
    resp = requests.get(
        API_URL,
        params={"ids": code, "format": "json"},
        timeout=REQUEST_TIMEOUT_SECONDS,
        headers={"User-Agent": "metar-reader-flask"},
    )
    resp.raise_for_status()
    # The API answers 204 / an empty body when the station is unknown.
    if resp.status_code == 204 or not resp.text.strip():
        return None
    data = resp.json()
    return data[0] if data else None


@app.route("/")
def index():
    """Render the search page, and the decoded report when a code is given.

    The airport code is read from the ``code`` query parameter. Invalid input,
    unknown airports and upstream failures are reported to the user as a
    friendly error message rather than an HTTP error.
    """
    code = (request.args.get("code") or "").strip().upper()
    report = error = None

    if code:
        # Validate before using the value in an outgoing request.
        if not AIRPORT_CODE_PATTERN.fullmatch(code):
            error = "Please enter a 3-4 character airport code, like KHIO."
        else:
            try:
                metar = fetch_metar(code)
                # US users often type 3-letter FAA codes (e.g. HIO); retry
                # with the "K" prefix to form the ICAO code (KHIO).
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
    # debug=True is for local development only; never enable it in production.
    app.run(debug=True)
