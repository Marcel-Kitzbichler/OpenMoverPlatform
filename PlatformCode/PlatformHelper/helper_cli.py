#!/usr/bin/env python3
"""
Enhanced CLI Platform Helper Tool for OpenMoverPlatform
Supports all serial communication intents (1-10)
"""

import serial
import json
import time
import sys
import os
from pathlib import Path

# Import existing modules
import parsekml


class PlatformCLI:
    def __init__(self, port_name, baudrate=115200):
        """Initialize serial connection to the platform"""
        try:
            self.ser = serial.Serial(
                port=port_name,
                baudrate=baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=2
            )
            print(f"Connected to {port_name} at {baudrate} baud")
        except Exception as e:
            print(f"Error connecting to port: {e}")
            sys.exit(1)

    def send_json(self, data):
        """Send JSON data to the platform"""
        json_str = json.dumps(data)
        self.ser.write(json_str.encode('utf-8'))
        print(f"Sent: {json_str}")

    def read_json(self, timeout=2):
        """Read JSON response from the platform"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.ser.in_waiting > 0:
                try:
                    line = self.ser.readline().decode('utf-8').strip()
                    if line:
                        return json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                except Exception as e:
                    print(f"Error reading: {e}")
            time.sleep(0.1)
        return None

    def intent_1_get_coordinates(self):
        """Intent 1: Get stored coordinates from platform"""
        print("\n=== Get Stored Coordinates ===")
        self.send_json({"intent": 1})
        response = self.read_json()
        if response:
            print(f"Response: {json.dumps(response, indent=2)}")
        else:
            print("No response received")

    def intent_2_execute_waypoints(self):
        """Intent 2: Execute waypoint navigation"""
        print("\n=== Execute Waypoint Navigation ===")
        confirm = input("Start waypoint navigation? (y/n): ")
        if confirm.lower() == 'y':
            self.send_json({"intent": 2})
            print("Waypoint navigation started")
        else:
            print("Cancelled")

    def intent_3_motor_control_mode(self):
        """Intent 3: Set motor control status"""
        print("\n=== Motor Control Mode ===")
        print("1. Enable direct motor control")
        print("2. Disable direct motor control")
        choice = input("Choice: ")
        
        if choice == '1':
            self.send_json({"intent": 3, "setStatus": True})
            print("Direct motor control enabled")
        elif choice == '2':
            self.send_json({"intent": 3, "setStatus": False})
            print("Direct motor control disabled")

    def intent_4_direct_motor_control(self):
        """Intent 4: Direct motor control"""
        print("\n=== Direct Motor Control ===")
        try:
            left_pwm = int(input("Left motor PWM (-255 to 255): "))
            right_pwm = int(input("Right motor PWM (-255 to 255): "))
            self.send_json({"intent": 4, "leftPWM": left_pwm, "rightPWM": right_pwm})
            print(f"Motors set to L:{left_pwm}, R:{right_pwm}")
        except ValueError:
            print("Invalid input")

    def intent_5_upload_coordinates(self):
        """Intent 5: Upload coordinates from KML file"""
        print("\n=== Upload Coordinates ===")
        kml_path = input("KML file path: ")
        
        if not Path(kml_path).exists():
            print("File not found")
            return
        
        try:
            kml_array = parsekml.parse(kml_path)
            kml_array.insert(0, len(kml_array) / 2)
            speed = float(input("Speed: "))
            range_val = float(input("Range: "))
            kml_array.insert(1, speed)
            kml_array.insert(2, range_val)
            
            self.send_json({"intent": 5, "coordinates": kml_array})
            print("Coordinates uploaded successfully")
        except Exception as e:
            print(f"Error: {e}")

    def intent_6_get_status(self):
        """Intent 6: Get platform status"""
        print("\n=== Platform Status ===")
        self.send_json({"intent": 6})
        response = self.read_json()
        
        if response:
            print("\nStatus Information:")
            print(f"  Battery Voltage: {response.get('batteryVoltage', 'N/A')} V")
            print(f"  GPS Satellites: {response.get('numSats', 'N/A')}")
            print(f"  GPS Fix: {response.get('fix', 'N/A')}")
            print(f"  Location Age: {response.get('locationAge', 'N/A')} ms")
            print(f"  Latitude: {response.get('lat', 'N/A')}")
            print(f"  Longitude: {response.get('lon', 'N/A')}")
            print(f"  Heading: {response.get('heading', 'N/A')}°")
            print(f"  Serial Control: {response.get('serialControl', 'N/A')}")
            print(f"  Motor Handled: {response.get('motorHandled', 'N/A')}")
            print(f"  Motor Setpoints: L={response.get('setPointL', 'N/A')}, R={response.get('setPointR', 'N/A')}")
            print(f"  Mag Calibration: X[{response.get('magXMin', 'N/A')}, {response.get('magXMax', 'N/A')}], Y[{response.get('magYMin', 'N/A')}, {response.get('magYMax', 'N/A')}]")
        else:
            print("No response received")

    def intent_7_goto_coordinate(self):
        """Intent 7: Go to single coordinate"""
        print("\n=== Go To Coordinate ===")
        try:
            lat = float(input("Latitude: "))
            lon = float(input("Longitude: "))
            speed = float(input("Speed: "))
            range_val = float(input("Range: "))
            
            self.send_json({
                "intent": 7,
                "lat": lat,
                "lon": lon,
                "speed": speed,
                "range": range_val
            })
            print(f"Navigating to ({lat}, {lon})")
        except ValueError:
            print("Invalid input")

    def intent_8_calibrate_compass(self):
        """Intent 8: Calibrate magnetometer/compass"""
        print("\n=== Calibrate Compass ===")
        print("This will start compass calibration routine.")
        print("Rotate the platform in all directions during calibration.")
        confirm = input("Start calibration? (y/n): ")
        
        if confirm.lower() == 'y':
            self.send_json({"intent": 8})
            print("Compass calibration started")
        else:
            print("Cancelled")

    def intent_9_log_mag_data(self):
        """Intent 9: Log magnetometer data"""
        print("\n=== Log Magnetometer Data ===")
        file_name = input("Output file name: ")
        print("Logging magnetometer data... Press Ctrl+C to stop")
        
        data_received = []
        try:
            while True:
                self.send_json({"intent": 9})
                response = self.read_json(timeout=1)
                
                if response:
                    data_received.append(response)
                    print(f"Mag: X={response.get('magX', 'N/A')}, Y={response.get('magY', 'N/A')}, "
                          f"Min/Max: X[{response.get('magXMin', 'N/A')}, {response.get('magXMax', 'N/A')}], "
                          f"Y[{response.get('magYMin', 'N/A')}, {response.get('magYMax', 'N/A')}]")
                
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping data logging...")
            with open(file_name, 'w') as f:
                json.dump(data_received, f, indent=2)
            print(f"Data saved to {file_name}")

    def intent_10_set_motor_bias(self):
        """Intent 10: Set motor bias correction"""
        print("\n=== Set Motor Bias ===")
        try:
            bias_l = float(input("Left motor bias: "))
            bias_r = float(input("Right motor bias: "))
            
            self.send_json({"intent": 10, "biasL": bias_l, "biasR": bias_r})
            print(f"Motor bias set to L:{bias_l}, R:{bias_r}")
        except ValueError:
            print("Invalid input")

    def print_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("OpenMoverPlatform - Enhanced CLI Helper")
        print("="*50)
        print(" 1. Get stored coordinates")
        print(" 2. Execute waypoint navigation")
        print(" 3. Set motor control mode")
        print(" 4. Direct motor control")
        print(" 5. Upload coordinates from KML")
        print(" 6. Get platform status")
        print(" 7. Go to single coordinate")
        print(" 8. Calibrate compass")
        print(" 9. Log magnetometer data")
        print("10. Set motor bias")
        print(" 0. Exit")
        print("="*50)

    def run(self):
        """Main CLI loop"""
        menu_actions = {
            '1': self.intent_1_get_coordinates,
            '2': self.intent_2_execute_waypoints,
            '3': self.intent_3_motor_control_mode,
            '4': self.intent_4_direct_motor_control,
            '5': self.intent_5_upload_coordinates,
            '6': self.intent_6_get_status,
            '7': self.intent_7_goto_coordinate,
            '8': self.intent_8_calibrate_compass,
            '9': self.intent_9_log_mag_data,
            '10': self.intent_10_set_motor_bias,
        }

        while True:
            try:
                self.print_menu()
                choice = input("\nChoice: ").strip()

                if choice == '0':
                    print("Exiting...")
                    self.ser.close()
                    break

                if choice in menu_actions:
                    menu_actions[choice]()
                else:
                    print("Invalid choice")

            except KeyboardInterrupt:
                print("\n\nExiting...")
                self.ser.close()
                break
            except Exception as e:
                print(f"Error: {e}")

    def close(self):
        """Close serial connection"""
        if self.ser and self.ser.is_open:
            self.ser.close()


def main():
    """Main entry point"""
    print("OpenMoverPlatform - Enhanced CLI Helper")
    print("-" * 50)
    
    # Get serial port
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = input("Serial port (e.g., COM3, /dev/ttyUSB0): ")
    
    # Create and run CLI
    cli = PlatformCLI(port)
    cli.run()


if __name__ == "__main__":
    main()
