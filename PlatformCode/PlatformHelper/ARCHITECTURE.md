# OpenMoverPlatform Helper Tools - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    PC Helper Applications                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  helper.py   │  │helper_cli.py │  │helper_gui.py │      │
│  │   (Legacy)   │  │  (Enhanced)  │  │   (Modern)   │      │
│  │              │  │              │  │              │      │
│  │ - Intent 5   │  │ - All 10     │  │ - All 10     │      │
│  │ - Intent 9   │  │   intents    │  │   intents    │      │
│  │              │  │ - Menu-based │  │ - Tabbed GUI │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                  │               │
│         └─────────────────┴──────────────────┘               │
│                           │                                  │
│                  ┌────────▼────────┐                         │
│                  │  parsekml.py    │                         │
│                  │  (KML Parser)   │                         │
│                  └─────────────────┘                         │
└────────────────────────────┬────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Serial / USB   │
                    │  (115200 baud)  │
                    │   JSON Messages │
                    └────────┬────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│              OpenMoverPlatform (ESP32 Firmware)              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              serialManager.cpp (Main Hub)               │ │
│  │                                                          │ │
│  │  Intent Router:                                         │ │
│  │  ┌──────────────────────────────────────────────────┐  │ │
│  │  │ Intent 1 → wpManager (get coordinates)          │  │ │
│  │  │ Intent 2 → wpManager (execute waypoints)        │  │ │
│  │  │ Intent 3 → motorSet (control mode)              │  │ │
│  │  │ Intent 4 → motorSet (direct control)            │  │ │
│  │  │ Intent 5 → wpManager (upload coordinates)       │  │ │
│  │  │ Intent 6 → Status aggregator (all sensors)      │  │ │
│  │  │ Intent 7 → goTo (single coordinate)             │  │ │
│  │  │ Intent 8 → compass (calibration)                │  │ │
│  │  │ Intent 9 → compass (magnetometer data)          │  │ │
│  │  │ Intent 10 → motorSet (bias correction)          │  │ │
│  │  └──────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ wpManager│  │ motorSet │  │  compass │  │  battery │   │
│  │          │  │          │  │          │  │          │   │
│  │ - Route  │  │ - PWM    │  │ - Mag    │  │ - Volt   │   │
│  │ - Nav    │  │ - Bias   │  │ - Calib  │  │ - Monitor│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                               │
│  ┌──────────┐  ┌──────────┐                                 │
│  │   goTo   │  │   GPS    │                                 │
│  │          │  │(TinyGPS++)                                 │
│  │ - Single │  │          │                                 │
│  │   Point  │  │ - Fix    │                                 │
│  │ - Nav    │  │ - Coords │                                 │
│  └──────────┘  └──────────┘                                 │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Communication Protocol

### Message Format

All messages are JSON objects sent over serial:

```
PC → Platform:  {"intent": N, ...parameters...}
Platform → PC:  {...response data...}
```

### Intent Flow Diagram

```
User Action → Helper Tool → JSON Message → Serial → Platform
                                                       ↓
                                               Intent Router
                                                       ↓
                          ┌────────────────────────────┴─────────────┐
                          ↓                                          ↓
                    Motor Control                              Navigation
                    ├─ Set Mode (3)                           ├─ Upload (5)
                    ├─ Direct (4)                             ├─ Execute (2)
                    └─ Bias (10)                              ├─ Get (1)
                                                               └─ GoTo (7)
                          ↓                                          ↓
                    Status/Data                                Calibration
                    └─ Status (6)                              ├─ Compass (8)
                                                               └─ Mag Data (9)
```

## Data Flow Examples

### Example 1: Upload and Execute Waypoints

```
1. User: Select KML file in GUI
2. helper_gui.py: Parse KML with parsekml.py
3. helper_gui.py: Format coordinates array
4. helper_gui.py: Send {"intent": 5, "coordinates": [...]}
5. serialManager.cpp: Receive and store in coordinateTable[]
6. User: Click "Execute Navigation" in GUI
7. helper_gui.py: Send {"intent": 2}
8. serialManager.cpp: Create wpManagerExec task
9. wpManager.cpp: Navigate through waypoints using GPS and compass
```

### Example 2: Real-time Status Monitoring

```
Loop every 1 second:
1. helper_gui.py: Send {"intent": 6}
2. serialManager.cpp: Collect data from all modules
3. serialManager.cpp: Send JSON response with:
   - Battery voltage (from battery.cpp)
   - GPS data (from TinyGPSPlus)
   - Heading (from compass.cpp)
   - Motor status (from motorSet.cpp)
   - Mag calibration (from compass.cpp)
4. helper_gui.py: Parse response and update UI
```

### Example 3: Compass Calibration

```
1. User: Click "Start Calibration" in GUI
2. helper_gui.py: Send {"intent": 8}
3. serialManager.cpp: Create calibrateMag task
4. compass.cpp: Start recording min/max magnetometer values
5. User: Physically rotates platform
6. compass.cpp: Continuously update min/max bounds
7. User: Check status {"intent": 6} to see calibration values
8. helper_gui.py: Display magXMin/Max, magYMin/Max
```

## Class/Module Responsibilities

### PC Side (Python)

| Module | Responsibility |
|--------|---------------|
| `helper_gui.py` | GUI interface, user interaction, tab management |
| `helper_cli.py` | CLI interface, menu system, user prompts |
| `helper.py` | Legacy simple CLI (backward compatibility) |
| `parsekml.py` | Parse KML files, extract coordinates |

### Platform Side (C++)

| Module | Responsibility |
|--------|---------------|
| `serialManager.cpp` | Message routing, JSON parsing, task creation |
| `wpManager.cpp` | Waypoint storage, route execution |
| `motorSet.cpp` | Motor control, PWM output, bias correction |
| `compass.cpp` | Magnetometer reading, calibration, heading |
| `battery.cpp` | Battery voltage monitoring |
| `goTo.cpp` | Single-point navigation logic |
| `emerg.cpp` | Emergency stop functionality |

## Threading Model (GUI)

```
Main Thread (GUI)
├─ UI Event Loop
├─ User Interactions
└─ Serial Communication

Background Threads:
├─ Auto-status Thread (when enabled)
│  └─ Polls status every 1 second
└─ Magnetometer Logging Thread (when active)
   └─ Logs mag data every 1 second
```

## State Management

### Platform States

```
┌──────────────┐
│   Idle       │◄──────┐
└──────┬───────┘       │
       │               │
       │ Intent 2/7    │ Complete/Stop
       ↓               │
┌──────────────┐       │
│ Navigating   │───────┘
└──────────────┘

┌──────────────┐
│Motor Control │
│  Disabled    │◄──────┐
└──────┬───────┘       │
       │               │
       │ Intent 3(true)│ Intent 3(false)
       ↓               │
┌──────────────┐       │
│Motor Control │───────┘
│   Enabled    │
└──────────────┘
```

## Extension Points

### Adding New Intents

1. **PC Side**: Add handler method in `helper_cli.py` and `helper_gui.py`
2. **Platform Side**: Add case in `serialManager.cpp` intent switch
3. **Documentation**: Update README.md with new intent details

### Adding New Data Sources

1. Create new module (e.g., `temperature.cpp`)
2. Add data collection in Intent 6 handler
3. Update GUI status tab to display new data
4. Document in protocol specification

### Custom Applications

The helper classes can be imported and used in custom Python applications:

```python
from helper_cli import PlatformCLI

class CustomController:
    def __init__(self, port):
        self.platform = PlatformCLI(port)
    
    def autonomous_mission(self):
        # Upload waypoints
        self.platform.intent_5_upload_coordinates()
        # Wait for GPS
        while not self.check_gps_ready():
            time.sleep(1)
        # Execute
        self.platform.intent_2_execute_waypoints()
```

## Security Considerations

- **Serial Access**: Requires appropriate permissions (dialout group on Linux)
- **Motor Control**: Emergency stop always available via Intent 3
- **JSON Parsing**: Error handling prevents malformed messages from crashing
- **Task Management**: Platform prevents multiple simultaneous navigation tasks

## Performance Characteristics

- **Serial Latency**: ~10-50ms typical
- **GPS Update Rate**: Configurable via GPSInterval (default shown in code)
- **Status Polling**: 1Hz typical for GUI auto-refresh
- **Task Priority**: Motor control runs on dedicated core (ESP32)

## Dependencies

### PC Side
- Python 3.7+
- pyserial 3.5+
- tkinter (for GUI, included with most Python installations)

### Platform Side
- Arduino Framework
- ArduinoJson library
- TinyGPSPlus library
- ESP32 board support

## File Structure

```
PlatformCode/
├── PlatformHelper/          # PC helper tools
│   ├── helper_gui.py        # Modern GUI application
│   ├── helper_cli.py        # Enhanced CLI application  
│   ├── helper.py            # Legacy CLI
│   ├── parsekml.py          # KML parser
│   ├── intent5.py           # Legacy intent 5
│   ├── intent9.py           # Legacy intent 9
│   ├── requirements.txt     # Python dependencies
│   ├── README.md            # Full documentation
│   ├── USAGE_EXAMPLES.md    # Usage examples
│   ├── QUICK_REFERENCE.md   # Quick reference
│   └── ARCHITECTURE.md      # This file
│
└── OpenMoverplatform/       # ESP32 firmware
    ├── src/
    │   ├── main.cpp
    │   ├── serialManager.cpp    # Main communication hub
    │   ├── wpManager.cpp        # Waypoint management
    │   ├── motorSet.cpp         # Motor control
    │   ├── compass.cpp          # Compass/magnetometer
    │   ├── battery.cpp          # Battery monitoring
    │   ├── goTo.cpp             # Single-point navigation
    │   └── emerg.cpp            # Emergency functions
    └── include/
        └── [corresponding .h files]
```

## Future Enhancement Ideas

1. **Telemetry Recording**: Full mission recording and replay
2. **Path Planning**: Automatic obstacle avoidance
3. **Web Interface**: Browser-based control panel
4. **Mobile App**: iOS/Android companion app
5. **Offline Maps**: Display platform position on map
6. **Mission Scripting**: Automated mission sequences
7. **Multi-Platform**: Control multiple platforms simultaneously
8. **Data Visualization**: Real-time plotting of sensor data
