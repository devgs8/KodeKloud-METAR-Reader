"""Turn aviationweather.gov METAR JSON records into plain English."""

WX_CODES = {
    "MI": "shallow", "BC": "patches of", "PR": "partial", "DR": "low drifting",
    "BL": "blowing", "SH": "showers of", "TS": "thunderstorm with", "FZ": "freezing",
    "DZ": "drizzle", "RA": "rain", "SN": "snow", "SG": "snow grains",
    "IC": "ice crystals", "PL": "ice pellets", "GR": "hail", "GS": "small hail",
    "UP": "unknown precipitation", "BR": "mist", "FG": "fog", "FU": "smoke",
    "VA": "volcanic ash", "DU": "dust", "SA": "sand", "HZ": "haze", "PY": "spray",
    "PO": "dust whirls", "SQ": "squalls", "FC": "funnel cloud", "SS": "sandstorm",
    "DS": "duststorm",
}
INTENSITY = {"-": "light", "+": "heavy"}
COVER = {
    "SKC": "clear skies", "CLR": "clear skies", "NSC": "no significant clouds",
    "FEW": "a few clouds", "SCT": "scattered clouds", "BKN": "mostly cloudy",
    "OVC": "overcast", "VV": "obscured sky",
}
FLIGHT_CAT = {
    "VFR": "VFR (good visibility, easy flying conditions)",
    "MVFR": "Marginal VFR (somewhat reduced visibility or low clouds)",
    "IFR": "IFR (poor visibility or low clouds)",
    "LIFR": "Low IFR (very poor visibility or very low clouds)",
}
COMPASS = ["north", "north-northeast", "northeast", "east-northeast", "east",
           "east-southeast", "southeast", "south-southeast", "south",
           "south-southwest", "southwest", "west-southwest", "west",
           "west-northwest", "northwest", "north-northwest"]


def c_to_f(c):
    return c * 9 / 5 + 32


def kt_to_mph(kt):
    return kt * 1.15078


def compass(deg):
    return COMPASS[int((deg % 360) / 22.5 + 0.5) % 16]


def decode_weather(wx):
    """Decode a present-weather string like '-RA BR' or '+TSRA'."""
    phrases = []
    for token in (wx or "").split():
        intensity = ""
        if token[0] in INTENSITY:
            intensity, token = INTENSITY[token[0]], token[1:]
        elif token.startswith("VC"):
            intensity, token = "nearby", token[2:]
        parts = [WX_CODES[token[i:i + 2]] for i in range(0, len(token), 2)
                 if token[i:i + 2] in WX_CODES]
        if parts:
            phrases.append(" ".join(p for p in [intensity] + parts if p))
    return phrases


def describe_wind(wdir, wspd, wgst):
    if not wspd:
        return "Calm winds"
    mph = round(kt_to_mph(wspd))
    if wdir in (None, "VRB"):
        text = f"Wind {mph} mph, direction variable"
    else:
        text = f"Wind {mph} mph from the {compass(wdir)}"
    if wgst:
        text += f", gusting to {round(kt_to_mph(wgst))} mph"
    return text


def describe_sky(clouds):
    if not clouds:
        return "Clear skies"
    parts = []
    for layer in clouds:
        cover = layer.get("cover", "")
        label = COVER.get(cover, cover)
        base = layer.get("base")
        if cover in ("SKC", "CLR", "NSC") or base is None:
            parts.append(label)
        else:
            parts.append(f"{label} at {base:,} ft")
    return ", ".join(parts).capitalize()


def describe_visibility(visib):
    if visib is None:
        return None
    if isinstance(visib, str):
        visib = float(visib.replace("+", ""))
        return f"Visibility {visib:g}+ miles"
    return f"Visibility {visib:g} mile{'s' if visib != 1 else ''}"


def headline(metar):
    """One friendly sentence, e.g. 'Light rain, 51°F, wind 3 mph from the southwest.'"""
    wx = decode_weather(metar.get("wxString"))
    if wx:
        cond = ", ".join(wx).capitalize()
    else:
        covers = [c["cover"] for c in (metar.get("clouds") or [])]
        if not covers or covers[0] in ("SKC", "CLR", "NSC"):
            cond = "Clear"
        else:
            worst = covers[-1] if covers[-1] in ("OVC", "VV") else covers[0]
            cond = COVER.get(worst, "Cloudy").capitalize()
    bits = [cond]
    if metar.get("temp") is not None:
        bits.append(f"{round(c_to_f(metar['temp']))}°F")
    wind = describe_wind(metar.get("wdir"), metar.get("wspd"), metar.get("wgst"))
    bits.append(wind[0].lower() + wind[1:])
    return ", ".join(bits) + "."


def decode(metar):
    """Return a dict of display-ready fields."""
    temp, dewp = metar.get("temp"), metar.get("dewp")
    details = []
    if temp is not None:
        t = f"{round(c_to_f(temp))}°F ({temp:g}°C)"
        if dewp is not None:
            t += f", dew point {round(c_to_f(dewp))}°F"
            if temp - dewp <= 2.5:
                t += " — humid; expect damp or foggy conditions"
        details.append(("Temperature", t))
    details.append(("Wind", describe_wind(metar.get("wdir"), metar.get("wspd"), metar.get("wgst"))))
    vis = describe_visibility(metar.get("visib"))
    if vis:
        details.append(("Visibility", vis))
    wx = decode_weather(metar.get("wxString"))
    if wx:
        details.append(("Weather", ", ".join(wx).capitalize()))
    details.append(("Sky", describe_sky(metar.get("clouds"))))
    if metar.get("altim") is not None:
        details.append(("Pressure", f"{metar['altim'] * 0.02953:.2f} inHg ({metar['altim']:g} hPa)"))
    cat = metar.get("fltCat")
    return {
        "station": metar.get("icaoId"),
        "name": metar.get("name"),
        "time": metar.get("reportTime"),
        "headline": headline(metar),
        "details": details,
        "flight_category": FLIGHT_CAT.get(cat, cat),
        "flight_cat_code": cat,
        "raw": metar.get("rawOb"),
    }
