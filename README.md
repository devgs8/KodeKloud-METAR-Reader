# METAR Reader

A small Flask web app that turns cryptic aviation weather reports (METARs) into plain English.

Type in an airport code and get a friendly summary like:

> **Light rain, mist, 51°F, calm winds.**

Below the headline you get the details: temperature and dew point, wind (with compass direction and gusts), visibility, weather, cloud layers, pressure, and the flight category (VFR/IFR). The original METAR is available in a collapsible section.

## What is a METAR?

A METAR is a standardized weather observation issued by airports, usually every hour. For example:

```
METAR KHIO 092153Z 00000KT 2 1/2SM -RA BR BKN004 OVC023 11/10 A2994
```

This app decodes that into "light rain and mist, 51°F, calm winds, mostly cloudy at 400 ft, visibility 2.5 miles".

## Features

- Search by ICAO code (`KHIO`, `EGLL`) or 3-letter US FAA code (`HIO`)
- Temperature in °F and °C, wind in mph with compass direction
- Decodes weather codes (`-RA BR` becomes "light rain, mist"), gusts and cloud layers
- Flight category badge (VFR, MVFR, IFR, LIFR)
- Responsive layout with dark mode
- No API key required

## Requirements

- Python 3.9 or newer
- An internet connection (weather data is fetched live)

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/devgs8/KodeKloud-METAR-Reader.git
cd KodeKloud-METAR-Reader

# 2. (Recommended) create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

Then open <http://127.0.0.1:5000> in your browser and enter an airport code.

On Windows, use `py app.py` if `python` is not on your PATH.

## Running the tests

```bash
python -m pytest
```

## Project structure

| File | Purpose |
| --- | --- |
| `app.py` | Flask app: handles the request, calls the weather API, renders the page |
| `decoder.py` | Converts METAR data into plain-English text |
| `templates/index.html` | The single web page |
| `tests/test_decoder.py` | Unit tests for the decoder |

## Data source

Weather data comes from the NOAA [Aviation Weather Center Data API](https://aviationweather.gov/data/api/). The service is free and requires no key.

## Disclaimer

This app is for general information only. **Do not use it for flight planning or any safety-critical decision.** Always consult official aviation weather sources.

## Deployment note

`app.py` starts Flask's development server with `debug=True`. For a public deployment, run the app behind a production WSGI server such as Gunicorn (`gunicorn app:app`) and disable debug mode.
