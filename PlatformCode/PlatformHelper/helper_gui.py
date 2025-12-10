#!/usr/bin/env python3
"""
Modern GUI Platform Helper Tool for OpenMoverPlatform
Features: Real-time status monitoring, motor control, waypoint management, compass calibration
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import serial
import serial.tools.list_ports
import json
import time
import threading
from pathlib import Path
import parsekml


class PlatformGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenMoverPlatform - Control Panel")
        self.root.geometry("1000x700")
        
        self.ser = None
        self.connected = False
        self.auto_status_running = False
        self.status_thread = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create tabs
        self.connection_tab = ttk.Frame(self.notebook)
        self.status_tab = ttk.Frame(self.notebook)
        self.motor_tab = ttk.Frame(self.notebook)
        self.waypoint_tab = ttk.Frame(self.notebook)
        self.compass_tab = ttk.Frame(self.notebook)
        self.log_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.connection_tab, text="Connection")
        self.notebook.add(self.status_tab, text="Status")
        self.notebook.add(self.motor_tab, text="Motor Control")
        self.notebook.add(self.waypoint_tab, text="Waypoints")
        self.notebook.add(self.compass_tab, text="Compass")
        self.notebook.add(self.log_tab, text="Console Log")
        
        # Setup each tab
        self.setup_connection_tab()
        self.setup_status_tab()
        self.setup_motor_tab()
        self.setup_waypoint_tab()
        self.setup_compass_tab()
        self.setup_log_tab()
        
    def setup_connection_tab(self):
        """Setup connection configuration tab"""
        frame = ttk.LabelFrame(self.connection_tab, text="Serial Connection", padding=10)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Port selection
        ttk.Label(frame, text="Serial Port:").grid(row=0, column=0, sticky='w', pady=5)
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(frame, textvariable=self.port_var, width=30)
        self.port_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Refresh Ports", command=self.refresh_ports).grid(row=0, column=2, padx=5, pady=5)
        
        # Baudrate
        ttk.Label(frame, text="Baudrate:").grid(row=1, column=0, sticky='w', pady=5)
        self.baudrate_var = tk.StringVar(value="115200")
        baudrate_combo = ttk.Combobox(frame, textvariable=self.baudrate_var, 
                                      values=["9600", "19200", "38400", "57600", "115200"], width=30)
        baudrate_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Connect button
        self.connect_btn = ttk.Button(frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.grid(row=2, column=0, columnspan=3, pady=20)
        
        # Status
        self.conn_status_label = ttk.Label(frame, text="Disconnected", foreground="red")
        self.conn_status_label.grid(row=3, column=0, columnspan=3)
        
        # Initial port refresh
        self.refresh_ports()
        
    def setup_status_tab(self):
        """Setup status monitoring tab"""
        frame = ttk.Frame(self.status_tab, padding=10)
        frame.pack(fill='both', expand=True)
        
        # Auto-refresh controls
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill='x', pady=5)
        
        self.auto_status_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(control_frame, text="Auto-refresh (1s interval)", 
                       variable=self.auto_status_var, 
                       command=self.toggle_auto_status).pack(side='left', padx=5)
        
        ttk.Button(control_frame, text="Refresh Now", 
                  command=self.get_status_once).pack(side='left', padx=5)
        
        # Status display in grid
        status_frame = ttk.LabelFrame(frame, text="Platform Status", padding=10)
        status_frame.pack(fill='both', expand=True, pady=5)
        
        # Create status labels
        self.status_labels = {}
        labels = [
            ("Battery Voltage", "batteryVoltage"),
            ("GPS Satellites", "numSats"),
            ("GPS Fix", "fix"),
            ("Location Age (ms)", "locationAge"),
            ("Latitude", "lat"),
            ("Longitude", "lon"),
            ("Heading (°)", "heading"),
            ("Serial Control", "serialControl"),
            ("Motor Handled", "motorHandled"),
            ("Motor L Setpoint", "setPointL"),
            ("Motor R Setpoint", "setPointR"),
            ("Mag X Range", "magXRange"),
            ("Mag Y Range", "magYRange"),
        ]
        
        for i, (label, key) in enumerate(labels):
            ttk.Label(status_frame, text=f"{label}:", font=('Arial', 10, 'bold')).grid(
                row=i, column=0, sticky='w', padx=5, pady=2)
            value_label = ttk.Label(status_frame, text="N/A", font=('Arial', 10))
            value_label.grid(row=i, column=1, sticky='w', padx=5, pady=2)
            self.status_labels[key] = value_label
            
    def setup_motor_tab(self):
        """Setup motor control tab"""
        frame = ttk.Frame(self.motor_tab, padding=10)
        frame.pack(fill='both', expand=True)
        
        # Motor control mode
        mode_frame = ttk.LabelFrame(frame, text="Motor Control Mode", padding=10)
        mode_frame.pack(fill='x', pady=5)
        
        ttk.Button(mode_frame, text="Enable Direct Control", 
                  command=lambda: self.set_motor_mode(True)).pack(side='left', padx=5)
        ttk.Button(mode_frame, text="Disable Direct Control", 
                  command=lambda: self.set_motor_mode(False)).pack(side='left', padx=5)
        
        # Direct motor control
        direct_frame = ttk.LabelFrame(frame, text="Direct Motor Control (PWM -255 to 255)", padding=10)
        direct_frame.pack(fill='x', pady=5)
        
        # Left motor
        ttk.Label(direct_frame, text="Left Motor:").grid(row=0, column=0, sticky='w', pady=5)
        self.motor_l_var = tk.IntVar(value=0)
        ttk.Scale(direct_frame, from_=-255, to=255, variable=self.motor_l_var, 
                 orient='horizontal', length=300).grid(row=0, column=1, padx=5)
        self.motor_l_label = ttk.Label(direct_frame, text="0")
        self.motor_l_label.grid(row=0, column=2, padx=5)
        self.motor_l_var.trace('w', lambda *args: self.motor_l_label.config(text=str(self.motor_l_var.get())))
        
        # Right motor
        ttk.Label(direct_frame, text="Right Motor:").grid(row=1, column=0, sticky='w', pady=5)
        self.motor_r_var = tk.IntVar(value=0)
        ttk.Scale(direct_frame, from_=-255, to=255, variable=self.motor_r_var, 
                 orient='horizontal', length=300).grid(row=1, column=1, padx=5)
        self.motor_r_label = ttk.Label(direct_frame, text="0")
        self.motor_r_label.grid(row=1, column=2, padx=5)
        self.motor_r_var.trace('w', lambda *args: self.motor_r_label.config(text=str(self.motor_r_var.get())))
        
        # Control buttons
        btn_frame = ttk.Frame(direct_frame)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="Set Motors", command=self.set_motors).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Stop Motors", command=self.stop_motors).pack(side='left', padx=5)
        
        # Motor bias
        bias_frame = ttk.LabelFrame(frame, text="Motor Bias Calibration", padding=10)
        bias_frame.pack(fill='x', pady=5)
        
        ttk.Label(bias_frame, text="Left Bias:").grid(row=0, column=0, sticky='w', pady=5)
        self.bias_l_var = tk.DoubleVar(value=1.0)
        ttk.Entry(bias_frame, textvariable=self.bias_l_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(bias_frame, text="Right Bias:").grid(row=1, column=0, sticky='w', pady=5)
        self.bias_r_var = tk.DoubleVar(value=1.0)
        ttk.Entry(bias_frame, textvariable=self.bias_r_var, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Button(bias_frame, text="Set Bias", command=self.set_motor_bias).grid(row=2, column=0, columnspan=2, pady=10)
        
    def setup_waypoint_tab(self):
        """Setup waypoint management tab"""
        frame = ttk.Frame(self.waypoint_tab, padding=10)
        frame.pack(fill='both', expand=True)
        
        # Upload from KML
        kml_frame = ttk.LabelFrame(frame, text="Upload Coordinates from KML", padding=10)
        kml_frame.pack(fill='x', pady=5)
        
        ttk.Label(kml_frame, text="KML File:").grid(row=0, column=0, sticky='w', pady=5)
        self.kml_path_var = tk.StringVar()
        ttk.Entry(kml_frame, textvariable=self.kml_path_var, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(kml_frame, text="Browse", command=self.browse_kml).grid(row=0, column=2, padx=5)
        
        ttk.Label(kml_frame, text="Speed:").grid(row=1, column=0, sticky='w', pady=5)
        self.kml_speed_var = tk.DoubleVar(value=1.0)
        ttk.Entry(kml_frame, textvariable=self.kml_speed_var, width=10).grid(row=1, column=1, sticky='w', padx=5)
        
        ttk.Label(kml_frame, text="Range:").grid(row=2, column=0, sticky='w', pady=5)
        self.kml_range_var = tk.DoubleVar(value=2.0)
        ttk.Entry(kml_frame, textvariable=self.kml_range_var, width=10).grid(row=2, column=1, sticky='w', padx=5)
        
        ttk.Button(kml_frame, text="Upload Coordinates", command=self.upload_kml).grid(row=3, column=0, columnspan=3, pady=10)
        
        # Single coordinate
        single_frame = ttk.LabelFrame(frame, text="Go To Single Coordinate", padding=10)
        single_frame.pack(fill='x', pady=5)
        
        ttk.Label(single_frame, text="Latitude:").grid(row=0, column=0, sticky='w', pady=5)
        self.goto_lat_var = tk.DoubleVar(value=0.0)
        ttk.Entry(single_frame, textvariable=self.goto_lat_var, width=15).grid(row=0, column=1, padx=5)
        
        ttk.Label(single_frame, text="Longitude:").grid(row=1, column=0, sticky='w', pady=5)
        self.goto_lon_var = tk.DoubleVar(value=0.0)
        ttk.Entry(single_frame, textvariable=self.goto_lon_var, width=15).grid(row=1, column=1, padx=5)
        
        ttk.Label(single_frame, text="Speed:").grid(row=2, column=0, sticky='w', pady=5)
        self.goto_speed_var = tk.DoubleVar(value=1.0)
        ttk.Entry(single_frame, textvariable=self.goto_speed_var, width=10).grid(row=2, column=1, sticky='w', padx=5)
        
        ttk.Label(single_frame, text="Range:").grid(row=3, column=0, sticky='w', pady=5)
        self.goto_range_var = tk.DoubleVar(value=2.0)
        ttk.Entry(single_frame, textvariable=self.goto_range_var, width=10).grid(row=3, column=1, sticky='w', padx=5)
        
        ttk.Button(single_frame, text="Go To Coordinate", command=self.goto_coordinate).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Waypoint execution
        exec_frame = ttk.LabelFrame(frame, text="Waypoint Execution", padding=10)
        exec_frame.pack(fill='x', pady=5)
        
        btn_frame = ttk.Frame(exec_frame)
        btn_frame.pack()
        ttk.Button(btn_frame, text="Get Stored Coordinates", command=self.get_coordinates).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Execute Waypoint Navigation", command=self.execute_waypoints).pack(side='left', padx=5)
        
    def setup_compass_tab(self):
        """Setup compass calibration tab"""
        frame = ttk.Frame(self.compass_tab, padding=10)
        frame.pack(fill='both', expand=True)
        
        # Calibration
        calib_frame = ttk.LabelFrame(frame, text="Compass Calibration", padding=10)
        calib_frame.pack(fill='x', pady=5)
        
        info_text = """Compass calibration procedure:
1. Click 'Start Calibration' button
2. Slowly rotate the platform in all directions (360° on all axes)
3. Continue for at least 30 seconds
4. The calibration will update the min/max magnetometer values
5. Check the status tab to verify calibration values

The platform will automatically update calibration parameters."""
        
        ttk.Label(calib_frame, text=info_text, justify='left', wraplength=600).pack(pady=10)
        ttk.Button(calib_frame, text="Start Calibration", command=self.start_calibration).pack(pady=10)
        
        # Magnetometer data logging
        log_frame = ttk.LabelFrame(frame, text="Magnetometer Data Logging", padding=10)
        log_frame.pack(fill='x', pady=5)
        
        ttk.Label(log_frame, text="Log File:").grid(row=0, column=0, sticky='w', pady=5)
        self.mag_log_var = tk.StringVar(value="mag_data.json")
        ttk.Entry(log_frame, textvariable=self.mag_log_var, width=30).grid(row=0, column=1, padx=5)
        
        btn_frame = ttk.Frame(log_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        self.mag_log_btn = ttk.Button(btn_frame, text="Start Logging", command=self.toggle_mag_logging)
        self.mag_log_btn.pack(side='left', padx=5)
        
        self.mag_logging = False
        self.mag_log_thread = None
        self.mag_data = []
        
    def setup_log_tab(self):
        """Setup console log tab"""
        frame = ttk.Frame(self.log_tab, padding=10)
        frame.pack(fill='both', expand=True)
        
        # Log display
        self.log_text = scrolledtext.ScrolledText(frame, height=30, width=100, state='disabled')
        self.log_text.pack(fill='both', expand=True, pady=5)
        
        # Clear button
        ttk.Button(frame, text="Clear Log", command=self.clear_log).pack(pady=5)
        
    def log_message(self, message):
        """Add message to log"""
        self.log_text.config(state='normal')
        self.log_text.insert('end', f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')
        
    def clear_log(self):
        """Clear the log"""
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', 'end')
        self.log_text.config(state='disabled')
        
    def refresh_ports(self):
        """Refresh available serial ports"""
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        self.port_combo['values'] = port_list
        if port_list:
            self.port_combo.current(0)
        self.log_message(f"Found {len(port_list)} serial port(s)")
        
    def toggle_connection(self):
        """Connect or disconnect from serial port"""
        if not self.connected:
            try:
                port = self.port_var.get()
                baudrate = int(self.baudrate_var.get())
                self.ser = serial.Serial(port, baudrate, timeout=2)
                self.connected = True
                self.connect_btn.config(text="Disconnect")
                self.conn_status_label.config(text=f"Connected to {port}", foreground="green")
                self.log_message(f"Connected to {port} at {baudrate} baud")
            except Exception as e:
                messagebox.showerror("Connection Error", f"Failed to connect: {e}")
                self.log_message(f"Connection failed: {e}")
        else:
            if self.ser:
                self.ser.close()
            self.connected = False
            self.auto_status_var.set(False)
            self.toggle_auto_status()
            self.connect_btn.config(text="Connect")
            self.conn_status_label.config(text="Disconnected", foreground="red")
            self.log_message("Disconnected")
            
    def send_json(self, data):
        """Send JSON data to platform"""
        if not self.connected or not self.ser:
            messagebox.showwarning("Not Connected", "Please connect to the platform first")
            return False
        
        try:
            json_str = json.dumps(data)
            self.ser.write(json_str.encode('utf-8'))
            self.log_message(f"Sent: {json_str}")
            return True
        except Exception as e:
            self.log_message(f"Send error: {e}")
            messagebox.showerror("Send Error", f"Failed to send data: {e}")
            return False
            
    def read_json(self, timeout=2):
        """Read JSON response from platform"""
        if not self.connected or not self.ser:
            return None
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.ser.in_waiting > 0:
                try:
                    line = self.ser.readline().decode('utf-8').strip()
                    if line:
                        data = json.loads(line)
                        self.log_message(f"Received: {line}")
                        return data
                except json.JSONDecodeError as e:
                    self.log_message(f"JSON decode error: {e}")
                except Exception as e:
                    self.log_message(f"Read error: {e}")
            time.sleep(0.1)
        return None
        
    def toggle_auto_status(self):
        """Toggle automatic status updates"""
        if self.auto_status_var.get():
            self.auto_status_running = True
            self.status_thread = threading.Thread(target=self.auto_status_loop, daemon=True)
            self.status_thread.start()
            self.log_message("Auto-status updates enabled")
        else:
            self.auto_status_running = False
            self.log_message("Auto-status updates disabled")
            
    def auto_status_loop(self):
        """Auto-refresh status loop"""
        while self.auto_status_running and self.connected:
            self.get_status_once()
            time.sleep(1)
            
    def get_status_once(self):
        """Get status from platform once"""
        if self.send_json({"intent": 6}):
            response = self.read_json()
            if response:
                self.update_status_display(response)
                
    def update_status_display(self, data):
        """Update status display with received data"""
        # Battery voltage
        battery = data.get('batteryVoltage')
        self.status_labels["batteryVoltage"].config(
            text=f"{battery} V" if battery != 'N/A' and battery is not None else "N/A")
        
        # Simple values
        self.status_labels["numSats"].config(text=str(data.get('numSats', 'N/A')))
        self.status_labels["fix"].config(text=str(data.get('fix', 'N/A')))
        self.status_labels["locationAge"].config(text=str(data.get('locationAge', 'N/A')))
        
        # GPS coordinates with formatting
        lat = data.get('lat')
        self.status_labels["lat"].config(
            text=f"{lat:.6f}" if isinstance(lat, (int, float)) else "N/A")
        lon = data.get('lon')
        self.status_labels["lon"].config(
            text=f"{lon:.6f}" if isinstance(lon, (int, float)) else "N/A")
        
        # Heading with formatting
        heading = data.get('heading')
        self.status_labels["heading"].config(
            text=f"{heading:.1f}" if isinstance(heading, (int, float)) else "N/A")
        
        # Status flags
        self.status_labels["serialControl"].config(text=str(data.get('serialControl', 'N/A')))
        self.status_labels["motorHandled"].config(text=str(data.get('motorHandled', 'N/A')))
        self.status_labels["setPointL"].config(text=str(data.get('setPointL', 'N/A')))
        self.status_labels["setPointR"].config(text=str(data.get('setPointR', 'N/A')))
        
        # Magnetometer ranges with formatting
        magXMin = data.get('magXMin')
        magXMax = data.get('magXMax')
        if isinstance(magXMin, (int, float)) and isinstance(magXMax, (int, float)):
            self.status_labels["magXRange"].config(text=f"[{magXMin:.1f}, {magXMax:.1f}]")
        else:
            self.status_labels["magXRange"].config(text="N/A")
        
        magYMin = data.get('magYMin')
        magYMax = data.get('magYMax')
        if isinstance(magYMin, (int, float)) and isinstance(magYMax, (int, float)):
            self.status_labels["magYRange"].config(text=f"[{magYMin:.1f}, {magYMax:.1f}]")
        else:
            self.status_labels["magYRange"].config(text="N/A")
        
    def set_motor_mode(self, enable):
        """Set motor control mode"""
        self.send_json({"intent": 3, "setStatus": enable})
        mode = "enabled" if enable else "disabled"
        messagebox.showinfo("Motor Mode", f"Direct motor control {mode}")
        
    def set_motors(self):
        """Set motor PWM values"""
        left = self.motor_l_var.get()
        right = self.motor_r_var.get()
        self.send_json({"intent": 4, "leftPWM": left, "rightPWM": right})
        
    def stop_motors(self):
        """Stop both motors"""
        self.motor_l_var.set(0)
        self.motor_r_var.set(0)
        self.set_motors()
        
    def set_motor_bias(self):
        """Set motor bias values"""
        bias_l = self.bias_l_var.get()
        bias_r = self.bias_r_var.get()
        self.send_json({"intent": 10, "biasL": bias_l, "biasR": bias_r})
        messagebox.showinfo("Motor Bias", f"Bias set to L:{bias_l}, R:{bias_r}")
        
    def browse_kml(self):
        """Browse for KML file"""
        filename = filedialog.askopenfilename(
            title="Select KML File",
            filetypes=[("KML Files", "*.kml"), ("All Files", "*.*")]
        )
        if filename:
            self.kml_path_var.set(filename)
            
    def upload_kml(self):
        """Upload coordinates from KML file"""
        kml_path = self.kml_path_var.get()
        if not Path(kml_path).exists():
            messagebox.showerror("Error", "KML file not found")
            return
        
        try:
            kml_array = parsekml.parse(kml_path)
            kml_array.insert(0, len(kml_array) // 2)
            speed = self.kml_speed_var.get()
            range_val = self.kml_range_var.get()
            kml_array.insert(1, speed)
            kml_array.insert(2, range_val)
            
            self.send_json({"intent": 5, "coordinates": kml_array})
            messagebox.showinfo("Success", f"Uploaded {(len(kml_array)-3)//2} coordinates")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload: {e}")
            
    def goto_coordinate(self):
        """Navigate to single coordinate"""
        lat = self.goto_lat_var.get()
        lon = self.goto_lon_var.get()
        speed = self.goto_speed_var.get()
        range_val = self.goto_range_var.get()
        
        self.send_json({
            "intent": 7,
            "lat": lat,
            "lon": lon,
            "speed": speed,
            "range": range_val
        })
        messagebox.showinfo("Navigation", f"Navigating to ({lat:.6f}, {lon:.6f})")
        
    def get_coordinates(self):
        """Get stored coordinates from platform"""
        if self.send_json({"intent": 1}):
            response = self.read_json()
            if response:
                messagebox.showinfo("Coordinates", f"Received:\n{json.dumps(response, indent=2)}")
                
    def execute_waypoints(self):
        """Execute waypoint navigation"""
        result = messagebox.askyesno("Execute Waypoints", 
                                     "Start waypoint navigation with stored coordinates?")
        if result:
            self.send_json({"intent": 2})
            
    def start_calibration(self):
        """Start compass calibration"""
        result = messagebox.askyesno("Calibrate Compass",
                                     "Start compass calibration?\n\n"
                                     "Rotate the platform in all directions during calibration.")
        if result:
            self.send_json({"intent": 8})
            messagebox.showinfo("Calibration", "Calibration started. Rotate the platform now.")
            
    def toggle_mag_logging(self):
        """Toggle magnetometer data logging"""
        if not self.mag_logging:
            self.mag_logging = True
            self.mag_data = []
            self.mag_log_btn.config(text="Stop Logging")
            self.mag_log_thread = threading.Thread(target=self.mag_logging_loop, daemon=True)
            self.mag_log_thread.start()
            self.log_message("Magnetometer logging started")
        else:
            self.mag_logging = False
            self.mag_log_btn.config(text="Start Logging")
            self.save_mag_data()
            
    def mag_logging_loop(self):
        """Magnetometer logging loop"""
        while self.mag_logging and self.connected:
            if self.send_json({"intent": 9}):
                response = self.read_json(timeout=1)
                if response:
                    self.mag_data.append(response)
            time.sleep(1)
            
    def save_mag_data(self):
        """Save magnetometer data to file"""
        try:
            filename = self.mag_log_var.get()
            with open(filename, 'w') as f:
                json.dump(self.mag_data, f, indent=2)
            messagebox.showinfo("Saved", f"Saved {len(self.mag_data)} samples to {filename}")
            self.log_message(f"Saved {len(self.mag_data)} magnetometer samples to {filename}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save: {e}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = PlatformGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
