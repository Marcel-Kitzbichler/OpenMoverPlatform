"""Simple KML parser to extract coordinates from a <LineString><coordinates>...</coordinates></LineString> block.

Returns a flat list of floats (e.g. [lon,lat,alt, lon,lat,alt, ...]).
This function is intentionally lightweight — it does not validate the KML
structure strictly but will raise useful errors if the expected block
is not found.
"""
from pathlib import Path
import re


def parse(kmlfilePath: str):
    text = Path(kmlfilePath).read_text(encoding='utf-8')

    # Try to find the coordinates block inside a LineString
    m = re.search(r"<LineString>.*?<coordinates>(.*?)</coordinates>.*?</LineString>", text, flags=re.DOTALL | re.IGNORECASE)
    if not m:
        # fallback: try to find any <coordinates>...</coordinates>
        m = re.search(r"<coordinates>(.*?)</coordinates>", text, flags=re.DOTALL | re.IGNORECASE)
        if not m:
            raise ValueError("No <coordinates> block found in KML file")

    coords_text = m.group(1)

    # coordinates may be separated by whitespace and/or commas; split on whitespace or commas
    parts = re.split(r"[\s,]+", coords_text.strip())
    # filter out empty strings
    parts = [p for p in parts if p != ""]

    # convert to floats; ignore trailing non-numeric tokens
    floats = []
    for p in parts:
        try:
            floats.append(float(p))
        except ValueError:
            # skip values that can't be parsed
            continue

    return floats