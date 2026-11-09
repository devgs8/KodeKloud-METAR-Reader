import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from decoder import compass, decode, decode_weather  # noqa: E402

KHIO = {"icaoId": "KHIO", "temp": 10.6, "dewp": 10, "wdir": 230, "wspd": 3, "visib": 2.5,
        "altim": 1014, "wxString": "RA BR", "fltCat": "IFR", "reportTime": "t",
        "clouds": [{"cover": "BKN", "base": 600}, {"cover": "OVC", "base": 4200}]}


def test_compass():
    assert compass(180) == "south" and compass(230) == "southwest"


def test_weather():
    assert decode_weather("-RA BR") == ["light rain", "mist"]
    assert decode_weather("+TSRA") == ["heavy thunderstorm with rain"]


def test_decode():
    r = decode(KHIO)
    assert "51°F" in r["headline"] and "rain" in r["headline"].lower()
    d = dict(r["details"])
    assert "southwest" in d["Wind"] and "600 ft" in d["Sky"]


def test_calm_clear():
    r = decode({"temp": 21, "wspd": 0, "clouds": []})
    assert r["headline"] == "Clear, 70°F, calm winds."
