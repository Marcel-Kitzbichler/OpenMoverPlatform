# OpenMoverPlatform Helper Tools

This directory contains helper tools for communicating with and controlling the OpenMoverPlatform via serial connection.

## Tools Available

### 1. Modern GUI Application (`helper_gui.py`) ⭐ **Recommended**

A modern, user-friendly graphical interface for controlling and monitoring the platform.

**Features:**
- 📡 **Connection Management**: Easy serial port selection and connection
- 📊 **Real-time Status Monitoring**: Auto-refreshing dashboard showing:
  - Battery voltage
  - GPS status (satellites, fix, location)
  - Heading/compass data
  - Motor status and setpoints
  - Magnetometer calibration values
- 🎮 **Motor Control**: Direct PWM control with sliders and bias calibration
- 🗺️ **Waypoint Management**: 
  - Upload coordinates from KML files
  - Navigate to single coordinates
  - Execute stored waypoint sequences
- 🧭 **Compass Calibration**: Start and monitor compass calibration
- 📝 **Data Logging**: Log magnetometer data for analysis
- 📋 **Console Log**: View all communication activity

**Usage:**
```bash
python helper_gui.py
```

### 2. Enhanced CLI Application (`helper_cli.py`)

A full-featured command-line interface supporting all platform functions.

**Features:**
- All 10 serial communication intents supported
- Interactive menu-driven interface
- Supports all platform operations

**Usage:**
```bash
python helper_cli.py [port]
# or
python helper_cli.py
```

### 3. Legacy CLI Tool (`helper.py`)

The original simple CLI tool with basic functionality (intents 5 and 9 only).

## Installation

1. Install Python 3.7 or higher
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Serial Communication Protocol

The platform uses JSON-based messages over serial (115200 baud by default) with an "intent" field to specify the operation:

### Intent 1: Get Stored Coordinates
Request stored coordinate data from platform.
```json
{"intent": 1}
```

### Intent 2: Execute Waypoint Navigation
Start autonomous navigation through stored waypoints.
```json
{"intent": 2}
```

### Intent 3: Set Motor Control Mode
Enable/disable direct motor control.
```json
{"intent": 3, "setStatus": true}
```

### Intent 4: Direct Motor Control
Set motor PWM values (-255 to 255).
```json
{"intent": 4, "leftPWM": 100, "rightPWM": 100}
```

### Intent 5: Upload Coordinates
Upload waypoint coordinates with speed and range parameters.
```json
{"intent": 5, "coordinates": [numCoords/2, speed, range, lat1, lon1, lat2, lon2, ...]}
```

### Intent 6: Get Platform Status
Request comprehensive status information.
```json
{"intent": 6}
```

**Response:**
```json
{
  "batteryVoltage": 12.5,
  "numSats": 8,
  "fix": true,
  "locationAge": 100,
  "lat": 48.123456,
  "lon": 11.654321,
  "heading": 90.5,
  "serialControl": false,
  "motorHandled": false,
  "magXMin": -500.0,
  "magXMax": 500.0,
  "magYMin": -500.0,
  "magYMax": 500.0,
  "setPointL": 0,
  "setPointR": 0
}
```

### Intent 7: Go To Single Coordinate
Navigate to a specific GPS coordinate.
```json
{"intent": 7, "lat": 48.123456, "lon": 11.654321, "speed": 1.0, "range": 2.0}
```

### Intent 8: Calibrate Compass
Start magnetometer calibration routine.
```json
{"intent": 8}
```

### Intent 9: Get Magnetometer Data
Request current magnetometer readings.
```json
{"intent": 9}
```

**Response:**
```json
{
  "magX": 123.45,
  "magY": -234.56,
  "magXMin": -500.0,
  "magXMax": 500.0,
  "magYMin": -500.0,
  "magYMax": 500.0
}
```

### Intent 10: Set Motor Bias
Set motor bias correction factors.
```json
{"intent": 10, "biasL": 1.0, "biasR": 0.95}
```

## KML File Format

The tools support Google Earth KML files for waypoint upload. The KML file should contain a LineString with coordinates:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <Placemark>
      <LineString>
        <coordinates>
          11.654321,48.123456,0
          11.654322,48.123457,0
          11.654323,48.123458,0
        </coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>
```

## Support Modules

### `parsekml.py`
Parses KML files and extracts coordinate data.

### `intent5.py`
Legacy module for uploading coordinates (used by `helper.py`).

### `intent9.py`
Legacy module for logging magnetometer data (used by `helper.py`).

## Tips

1. **Connection Issues**: 
   - Ensure the platform is powered on and connected
   - Check that the correct serial port is selected
   - Verify baudrate is set to 115200

2. **Motor Control**:
   - Always enable direct motor control mode before using PWM control
   - Use motor bias to compensate for differences between motors
   - Stop motors before switching modes

3. **GPS Navigation**:
   - Ensure GPS has a fix (at least 4 satellites) before navigation
   - Set appropriate speed and range values for your terrain
   - Monitor status during navigation

4. **Compass Calibration**:
   - Perform in an area away from magnetic interference
   - Rotate slowly and completely in all directions
   - Verify min/max values in status display

## Troubleshooting

**GUI won't start:**
- Ensure tkinter is installed: `python -m tkinter`
- On Linux, you may need: `sudo apt-get install python3-tk`

**Serial connection fails:**
- Check port permissions on Linux: `sudo usermod -a -G dialout $USER`
- On Windows, check Device Manager for correct COM port

**No response from platform:**
- Verify platform firmware is running
- Check serial baudrate matches (115200)
- Try reconnecting

## Development

The serial communication protocol is defined in the platform firmware:
- `PlatformCode/OpenMoverplatform/src/serialManager.cpp`
- `PlatformCode/OpenMoverplatform/include/serialManager.h`

## License

See the repository LICENSE file for licensing information.
