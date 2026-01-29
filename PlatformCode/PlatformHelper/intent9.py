"""Continuously request magnetometer data (intent 9) and log results.

Usage: call `process(port)` interactively. Press Ctrl-C to stop logging;
the data is written to a JSON file on exit. A timestamped default filename
is provided if the user doesn't specify one.
"""
import json
import time
import datetime
import os


def _extract_json_from_text(text: str):
    s = text.find('{')
    e = text.rfind('}')
    if s != -1 and e != -1 and e > s:
        try:
            return json.loads(text[s:e+1])
        except json.JSONDecodeError:
            return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def process(port, filename: str = None, include_timestamp: bool = False, interval: float = 1.0):
    """Start logging magnetometer data until interrupted by the user.

    Parameters:
      - port: serial port object
      - filename: optional output filename (JSON). If omitted a timestamped
        filename `maglog_<iso>.json` will be used.
      - include_timestamp: if True, each record will get a `_ts` field.
      - interval: seconds between requests (default 1.0)
    """
    if filename is None or filename.strip() == "":
        now = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        filename = f"maglog_{now}.json"

    data_received = []
    print("Starting magnetometer logging. Press Ctrl-C to stop.")
    try:
        while True:
            payload = {"intent": 9}
            port.write(json.dumps(payload).encode('utf-8'))
            raw = port.readline()
            if not raw:
                time.sleep(interval)
                continue
            try:
                text = raw.decode('utf-8', errors='replace').strip()
            except Exception:
                time.sleep(interval)
                continue

            obj = _extract_json_from_text(text)
            if obj is None:
                # give a short debug print of the line received
                print("(non-json line) ", text)
                time.sleep(interval)
                continue

            if include_timestamp:
                obj['_ts'] = datetime.datetime.utcnow().isoformat() + 'Z'

            data_received.append(obj)
            print(obj)
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nLogging stopped by user.")

    # Persist the collected data
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_received, f, indent=2)
        print(f"Wrote {len(data_received)} records to {filename}")
    except Exception as e:
        print("Error writing log file:", e)

