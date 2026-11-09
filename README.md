# 🌦️ METAR Reader

METAR Reader is a small Flask web app that turns cryptic aviation weather reports into plain English. Type in an airport code and it fetches the latest METAR from the NOAA Aviation Weather Center, decodes it, and shows a friendly summary like "Light rain, mist, 51°F, calm winds", with temperature, wind, visibility, clouds and pressure explained underneath.

[![Demo](https://img.shields.io/badge/demo-run%20locally-blue)](#-usage)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

## 📡 What is METAR?

A METAR is a standardized weather observation issued by airports, usually every hour. It is compact and cryptic, which is great for pilots and hard for everyone else.

**Raw METAR (Hillsboro, Oregon):**

```text
METAR KHIO 092153Z 00000KT 2 1/2SM -RA BR BKN004 OVC023 11/10 A2994
```

**Plain English:**

> Light rain, mist, 51°F, calm winds. Visibility 2.5 miles. Mostly cloudy at 400 ft, overcast at 2,300 ft. Pressure 29.94 inHg.

## ✨ Features

- 🌍 **Global airport support**: search by ICAO code (`KHIO`, `EGLL`) or 3-letter US FAA code (`HIO`)
- 📱 **Responsive design**: works on phones and desktops, with automatic dark mode
- 🌡️ **Temperature conversion**: °F and °C, plus dew point and a humidity hint
- 🧭 **Wind direction**: speed in mph, compass direction ("from the southwest") and gusts
- ☁️ **Cloud coverage**: each layer explained, with its height in feet
- 🌧️ **Weather phenomena**: codes like `-RA BR` become "light rain, mist"
- ⏱️ **Real-time data**: fetched live from aviationweather.gov, no API key needed
- 🛡️ **Error handling**: friendly messages for invalid codes, unknown airports and network problems

## 🖼️ Screenshots

![METAR Reader screenshot](docs/screenshot.png)

## 🚀 Installation

Requires Python 3.8 or newer and an internet connection.

### Windows (PowerShell)

```powershell
git clone https://github.com/devgs8/KodeKloud-METAR-Reader.git
cd KodeKloud-METAR-Reader
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

### Linux / macOS

```bash
git clone https://github.com/devgs8/KodeKloud-METAR-Reader.git
cd KodeKloud-METAR-Reader
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## 💻 Usage

1. Start the app with `python app.py`.
2. Open <http://127.0.0.1:5000> in your browser.
3. Enter an airport code such as `KHIO`, `KJFK` or `EGLL` and press **Get weather**.

## 📁 Project structure

```text
KodeKloud-METAR-Reader/
├── app.py                 # Flask app: request handling, API call, page rendering
├── decoder.py             # Converts METAR data into plain-English text
├── templates/
│   └── index.html         # The single web page
├── tests/
│   └── test_decoder.py    # Unit tests for the decoder
├── docs/
│   └── screenshot.png     # README screenshot
├── requirements.txt
└── LICENSE
```

## 🧪 Running tests

```bash
python -m pytest
```

## 🔗 Data source

Weather data comes from the NOAA Aviation Weather Center [Data API](https://aviationweather.gov/data/api/) at [aviationweather.gov](https://aviationweather.gov). It is free and requires no key.

> **Disclaimer:** for general information only. Do not use it for flight planning or any safety-critical decision.

## 📄 License

Released under the [MIT License](LICENSE). © 2026 Geraldo Silva.
