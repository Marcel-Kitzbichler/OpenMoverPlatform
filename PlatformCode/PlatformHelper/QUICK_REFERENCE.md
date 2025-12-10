# Quick Reference Card - OpenMoverPlatform Helper Tools

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Launch GUI (recommended)
python helper_gui.py

# Launch CLI
python helper_cli.py /dev/ttyUSB0
```

## 📋 Intent Reference

| Intent | Function | GUI Tab | CLI Menu |
|--------|----------|---------|----------|
| 1 | Get stored coordinates | Waypoints | 1 |
| 2 | Execute waypoint navigation | Waypoints | 2 |
| 3 | Set motor control mode | Motor Control | 3 |
| 4 | Direct motor control | Motor Control | 4 |
| 5 | Upload coordinates from KML | Waypoints | 5 |
| 6 | Get platform status | Status | 6 |
| 7 | Go to single coordinate | Waypoints | 7 |
| 8 | Calibrate compass | Compass | 8 |
| 9 | Get/log magnetometer data | Compass | 9 |
| 10 | Set motor bias | Motor Control | 10 |

## 🎮 Common Commands (CLI)

```
6  → Check status
5  → Upload waypoints from KML
2  → Start navigation
3  → Enable/disable motor control
4  → Control motors manually
8  → Calibrate compass
9  → Log magnetometer data
10 → Set motor bias
0  → Exit
```

## 📊 Status Indicators

### Battery
- **>12V**: Good
- **11-12V**: Medium
- **<11V**: Low - return to charge

### GPS
- **Fix: true, Sats ≥4**: Ready for navigation
- **Fix: false**: Wait for satellite lock
- **Location Age >1000ms**: GPS data stale

### Motors
- **motorHandled: false**: Available for commands
- **motorHandled: true**: Busy (navigation active)
- **serialControl: true**: Manual control enabled

## ⚙️ Typical Workflows

### Autonomous Navigation
```
1. Upload waypoints (Intent 5)
2. Verify GPS fix (Intent 6)
3. Start navigation (Intent 2)
4. Monitor progress (Intent 6)
```

### Manual Control
```
1. Enable control (Intent 3)
2. Set motors (Intent 4)
3. Stop motors (Intent 4, PWM=0)
4. Disable control (Intent 3)
```

### Compass Calibration
```
1. Start calibration (Intent 8)
2. Rotate platform 30-60s
3. Check values (Intent 6)
4. Verify symmetry
```

## 🔧 Parameter Guidelines

| Parameter | Typical Range | Notes |
|-----------|--------------|-------|
| Speed | 0.5 - 2.0 | Lower = more accurate |
| Range | 1.5 - 3.0 m | Based on GPS accuracy |
| Motor PWM | -255 to 255 | Start low (50-100) |
| Motor Bias | 0.8 - 1.2 | Typically near 1.0 |

## 🚨 Safety Checklist

- [ ] Battery >11V
- [ ] GPS fix with 4+ satellites
- [ ] Clear, open test area
- [ ] Emergency stop ready
- [ ] Motors respond to stop command
- [ ] Calibrated compass (if navigating)

## 🐛 Quick Troubleshooting

| Problem | Quick Fix |
|---------|-----------|
| Won't connect | Check port, baudrate, permissions |
| No GPS fix | Move to open area, wait 1-2 min |
| Drifts left/right | Adjust motor bias (Intent 10) |
| Won't navigate | Check GPS fix & motorHandled status |
| Compass wrong | Recalibrate (Intent 8) |
| Circles in place | Balance motor bias |

## 📡 Serial Settings

- **Baudrate**: 115200
- **Data bits**: 8
- **Parity**: None
- **Stop bits**: 1
- **Format**: JSON over serial

## 🔗 File Locations

```
PlatformCode/PlatformHelper/
├── helper_gui.py           # Modern GUI (recommended)
├── helper_cli.py           # Enhanced CLI
├── helper.py               # Legacy CLI
├── README.md               # Full documentation
├── USAGE_EXAMPLES.md       # Detailed examples
├── QUICK_REFERENCE.md      # This file
└── requirements.txt        # Dependencies
```

## 💡 Pro Tips

1. **Use GUI for learning**: Visual feedback helps understanding
2. **Use CLI for automation**: Easier to script
3. **Monitor status frequently**: Catch issues early
4. **Log first navigation**: Review data for tuning
5. **Test waypoints individually**: Before running full route
6. **Keep backup coordinates**: In case of upload failure

## 📞 Getting Help

1. Check `README.md` for protocol details
2. Review `USAGE_EXAMPLES.md` for scenarios
3. Examine `serialManager.cpp` for firmware behavior
4. Open GitHub issue for bugs/features

---

**Remember**: Always test in safe areas first! 🛡️
