"""Request and display system information from the device (intent 6).

`process(ser, single_shot=False, timeout=3.0)` can be used interactively
or programmatically: if `single_shot=True` the function will request once
and return the parsed JSON (or None on timeout).
"""
import json
import time
import os
from typing import Optional


def _read_json_from_lines(lines):
    """Try to extract a JSON object from the given text lines.

    Returns parsed object or None.
    """
    for text in lines:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            s = text.find('{')
            e = text.rfind('}')
            if s != -1 and e != -1 and e > s:
                try:
                    return json.loads(text[s:e+1])
                except json.JSONDecodeError:
                    continue
    return None


def process(ser, single_shot: bool = False, timeout: float = 3.0) -> Optional[dict]:
    """Send intent 6 and parse the first valid JSON response.

    If `single_shot` is False the function behaves interactively and will
    allow repeated requests until the user chooses to return.
    """
    while True:
        payload = {"intent": 6}
        ser.write(json.dumps(payload).encode('utf-8'))
        start_time = time.time()
        collected = []

        while time.time() - start_time < timeout:
            line = ser.readline()
            if not line:
                time.sleep(0.02)
                continue
            try:
                text = line.decode('utf-8', errors='replace').strip()
            except Exception:
                continue
            if not text:
                continue
            collected.append(text)
            obj = _read_json_from_lines([text])
            if obj is not None:
                if single_shot:
                    return obj
                os.system('cls' if os.name == 'nt' else 'clear')
                print("System information:")
                print(json.dumps(obj, indent=2))
                break

        # timed out or displayed
        if single_shot:
            print("No valid JSON response within timeout.")
            return None

        choice = input("Press Enter to request another package, or type 'r' to return/exit: ").strip().lower()
        if choice in ('r', 'return', 'q', 'exit'):
            return None
        # otherwise loop and request again