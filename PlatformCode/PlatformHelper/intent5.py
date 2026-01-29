"""Upload coordinates parsed from a KML file to the device (intent 5).

This module intentionally keeps a simple `process(port, ...)` signature
so it can be used interactively or programmatically by the CLI helper.
"""
import json
from pathlib import Path
import parsekml


def process(port, kml_path: str = None, speed: float = None, range_m: float = None):
    """Parse a KML and send intent 5 payload to `port`.

    If `kml_path`, `speed` or `range_m` are omitted the function will
    prompt the user interactively.
    """
    if kml_path is None:
        kml_path = input("KML file path?: ").strip()

    coords = parsekml.parse(kml_path)
    if not coords:
        print("No coordinates parsed from KML.")
        return

    # number of coordinate pairs (assume coords is a flat list)
    count = len(coords) // 2

    if speed is None:
        while True:
            try:
                speed = float(input("Speed?: ").strip())
                break
            except Exception:
                print("Invalid number, try again.")

    if range_m is None:
        while True:
            try:
                range_m = float(input("Range?: ").strip())
                break
            except Exception:
                print("Invalid number, try again.")

    payload = {"intent": 5, "coordinates": []}
    # keep same layout as the device expects: [count, speed, range, ...coords]
    payload["coordinates"].append(int(count))
    payload["coordinates"].append(float(speed))
    payload["coordinates"].append(float(range_m))
    payload["coordinates"].extend(coords)

    data = json.dumps(payload).encode("utf-8")
    print(f"Sending {len(data)} bytes to device...")
    port.write(data)
    print("Data sent")