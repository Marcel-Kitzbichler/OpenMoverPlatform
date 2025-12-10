# OpenMoverPlatform Helper Tools - Usage Examples

## Quick Start

### Using the GUI (Recommended for beginners)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Launch the GUI:
```bash
python helper_gui.py
```

3. Connect to your platform:
   - Select serial port from dropdown (click "Refresh Ports" to update)
   - Click "Connect"
   - Navigate to different tabs to access features

### Using the Enhanced CLI

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Launch the CLI:
```bash
python helper_cli.py
# or specify port directly:
python helper_cli.py /dev/ttyUSB0
```

3. Select operations from the menu (1-10)

## Common Use Cases

### 1. Monitoring Platform Status

**GUI Method:**
1. Go to "Status" tab
2. Check "Auto-refresh" to enable real-time monitoring
3. View battery, GPS, heading, and motor status

**CLI Method:**
```
Choice: 6
```
This will display all status information.

### 2. Uploading Waypoints from KML

**GUI Method:**
1. Go to "Waypoints" tab
2. Click "Browse" to select your KML file
3. Set Speed and Range parameters
4. Click "Upload Coordinates"

**CLI Method:**
```
Choice: 5
KML file path: /path/to/waypoints.kml
Speed: 1.0
Range: 2.0
```

**Sample KML File** (`example_route.kml`):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Example Route</name>
    <Placemark>
      <name>Route Path</name>
      <LineString>
        <coordinates>
          11.5643210,48.1234560,0
          11.5643220,48.1234570,0
          11.5643230,48.1234580,0
          11.5643240,48.1234590,0
          11.5643250,48.1234600,0
        </coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>
```

### 3. Navigating to a Single Location

**GUI Method:**
1. Go to "Waypoints" tab
2. Enter Latitude and Longitude
3. Set Speed and Range
4. Click "Go To Coordinate"

**CLI Method:**
```
Choice: 7
Latitude: 48.123456
Longitude: 11.654321
Speed: 1.0
Range: 2.0
```

### 4. Manual Motor Control

**GUI Method:**
1. Go to "Motor Control" tab
2. Click "Enable Direct Control"
3. Adjust Left/Right motor sliders
4. Click "Set Motors"
5. Use "Stop Motors" to halt

**CLI Method:**
```
# First enable motor control
Choice: 3
Choice: 1

# Then control motors
Choice: 4
Left motor PWM (-255 to 255): 100
Right motor PWM (-255 to 255): 100

# To stop motors
Choice: 4
Left motor PWM (-255 to 255): 0
Right motor PWM (-255 to 255): 0
```

### 5. Calibrating the Compass

**GUI Method:**
1. Go to "Compass" tab
2. Click "Start Calibration"
3. Rotate the platform slowly in all directions for 30+ seconds
4. Check "Status" tab to see updated calibration values

**CLI Method:**
```
Choice: 8
Start calibration? (y/n): y

# Then physically rotate the platform
# Check calibration values:
Choice: 6
```

### 6. Logging Magnetometer Data

**GUI Method:**
1. Go to "Compass" tab
2. Enter filename for log
3. Click "Start Logging"
4. Wait for desired duration
5. Click "Stop Logging"

**CLI Method:**
```
Choice: 9
Output file name: compass_data.json
Logging magnetometer data... Press Ctrl+C to stop

# Press Ctrl+C when done
```

### 7. Setting Motor Bias for Straight Driving

If your platform tends to drift left or right, use motor bias:

**GUI Method:**
1. Go to "Motor Control" tab
2. Adjust Left/Right Bias values (e.g., 1.0 and 0.95)
3. Click "Set Bias"

**CLI Method:**
```
Choice: 10
Left motor bias: 1.0
Right motor bias: 0.95
```

### 8. Executing Autonomous Waypoint Navigation

**Complete Workflow:**

1. Upload waypoints (Intent 5):
```
Choice: 5
KML file path: route.kml
Speed: 1.0
Range: 2.0
```

2. Verify coordinates stored:
```
Choice: 1
```

3. Check GPS status:
```
Choice: 6
# Verify GPS fix is true and satellites >= 4
```

4. Start navigation:
```
Choice: 2
Start waypoint navigation? (y/n): y
```

5. Monitor during execution:
```
Choice: 6
# Repeatedly check status
```

## Tips & Best Practices

### GPS Navigation
- Always wait for GPS fix before navigation (4+ satellites)
- Set speed conservatively (0.5-2.0 range)
- Set range based on GPS accuracy (usually 1.5-3.0 meters)
- Test with single coordinate before full route

### Motor Control
- Start with low PWM values (50-100) to test
- Always have emergency stop accessible
- Calibrate motor bias on flat, level ground
- Disable direct control before autonomous navigation

### Compass Calibration
- Calibrate away from buildings and metal objects
- Rotate slowly and smoothly
- Cover all axes (pitch, roll, yaw)
- Verify min/max values are symmetric
- Recalibrate if environment changes significantly

### Data Logging
- Use descriptive filenames with timestamps
- Log during calibration for analysis
- Keep log durations reasonable (1-5 minutes)
- Review JSON data with your preferred tool

## Troubleshooting Examples

### Problem: Platform doesn't move
**Solution:**
```
# Check motor control status
Choice: 6
# Look for "serialControl" and "motorHandled"

# If serialControl is true, disable it
Choice: 3
Choice: 2  # Disable

# Try waypoint navigation again
```

### Problem: Platform circles instead of going straight
**Solution:**
```
# Set motor bias
Choice: 10
Left motor bias: 1.0
Right motor bias: 0.95  # Adjust this value

# Test and adjust iteratively
```

### Problem: GPS location not updating
**Solution:**
```
# Check GPS status
Choice: 6
# Look at "numSats", "fix", "locationAge"

# If locationAge is high or fix is false:
# - Move to open area
# - Wait for satellite acquisition
# - Check antenna connection
```

### Problem: Compass heading incorrect
**Solution:**
```
# Recalibrate compass
Choice: 8
Start calibration? (y/n): y

# Rotate platform for 30-60 seconds
# Then verify:
Choice: 6
# Check magXMin/Max and magYMin/Max values
```

## Integration with Custom Applications

You can import and use the helper classes in your own Python applications:

```python
from helper_cli import PlatformCLI

# Connect to platform
platform = PlatformCLI('/dev/ttyUSB0')

# Get status
platform.send_json({"intent": 6})
status = platform.read_json()
print(f"Battery: {status['batteryVoltage']}V")

# Set motors
platform.send_json({"intent": 3, "setStatus": True})
platform.send_json({"intent": 4, "leftPWM": 100, "rightPWM": 100})

# Clean up
platform.close()
```

## Safety Reminders

⚠️ **Always**:
- Have an emergency stop method ready
- Test in safe, open areas first
- Monitor battery voltage
- Maintain line of sight with platform
- Stop motors before mode changes

⚠️ **Never**:
- Operate near water, cliffs, or roads
- Leave autonomous operation unmonitored
- Operate with low battery
- Use in crowded areas
- Ignore error messages

## Additional Resources

- See `README.md` for detailed protocol documentation
- Check `serialManager.cpp` in firmware for protocol implementation
- Join community discussions for support
- Report bugs via GitHub issues
