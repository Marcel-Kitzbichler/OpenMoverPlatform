import serial
import json
import time
import os
import intent5
import intent6
import intent9


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def open_serial():
    port = input("Bot Serial Port (e.g. COM3): ")
    try:
        ser = serial.Serial(
            port=port,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1,
        )
        print(f"Opened serial port {port} at 115200")
        return ser
    except Exception as e:
        print("Failed to open serial port:", e)
        return None


def send_json(ser, obj):
    data = json.dumps(obj).encode('utf-8')
    ser.write(data)


def read_json_response(ser, timeout=2.0):
    start = time.time()
    collected = []
    while time.time() - start < timeout:
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
        # try full-line JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # try extract {...}
            s = text.find('{')
            e = text.rfind('}')
            if s != -1 and e != -1 and e > s:
                try:
                    return json.loads(text[s:e+1])
                except json.JSONDecodeError:
                    pass
    # timed out
    if collected:
        print("Received (incomplete) lines:")
        for l in collected:
            print("  ", l)
    return None


def pretty_print(obj):
    try:
        print(json.dumps(obj, indent=2))
    except Exception:
        print(obj)


def menu(ser):
    while True:
        clear()
        print("=== OpenMoverPlatform Helper ===")
        print("Serial:", ser.port)
        print()
        print(" 1) Request stored coordinates from device (intent 1)")
        print(" 2) Start waypoint navigation (intent 2)")
        print(" 3) Stop navigation / set direct motor control (intent 3)")
        print(" 4) Direct motor control (intent 4)")
        print(" 5) Upload coordinates from KML (intent 5)")
        print(" 6) Get system information (intent 6)")
        print(" 7) Execute single GoTo (intent 7)")
        print(" 8) Calibrate compass (intent 8)")
        print(" 9) Log magnetometer data (intent 9)")
        print("10) Set motor bias (intent 10)")
        print(" 0) Exit")
        try:
            choice = int(input('\nChoice: ').strip())
        except Exception:
            continue

        if choice == 0:
            print("Exiting helper.")
            break

        if choice == 1:
            send_json(ser, {"intent": 1})
            resp = read_json_response(ser, timeout=2.0)
            if resp is None:
                print("No response received.")
            else:
                pretty_print(resp)
                if "coordinates" in resp:
                    save = input("Save coordinates to file? (y/N): ").strip().lower()
                    if save == 'y':
                        fn = input("Filename: ").strip()
                        with open(fn, 'w') as f:
                            json.dump(resp["coordinates"], f)
                        print("Saved to", fn)
            input("Press Enter to continue...")

        elif choice == 2:
            send_json(ser, {"intent": 2})
            print("Start command sent.")
            input("Press Enter to continue...")

        elif choice == 3:
            val = input("Set direct serial motor control? (y/N): ").strip().lower()
            status = True if val == 'y' else False
            send_json(ser, {"intent": 3, "setStatus": status})
            print("Command sent.")
            input("Press Enter to continue...")

        elif choice == 4:
            try:
                left = int(input("Left PWM (int): "))
                right = int(input("Right PWM (int): "))
            except Exception:
                print("Invalid value(s).")
                input("Press Enter to continue...")
                continue
            send_json(ser, {"intent": 4, "leftPWM": left, "rightPWM": right})
            print("PWM set sent.")
            input("Press Enter to continue...")

        elif choice == 5:
            print("Upload coordinates from KML file")
            intent5.process(ser)
            input("Upload finished. Press Enter to continue...")

        elif choice == 6:
            print("Requesting system information (intent 6) — will display and allow repeated requests.")
            intent6.process(ser)
            input("Returned to menu. Press Enter to continue...")

        elif choice == 7:
            try:
                lat = float(input("Latitude: "))
                lon = float(input("Longitude: "))
                speed = float(input("Speed: "))
                rng = float(input("Range: "))
            except Exception:
                print("Invalid numeric input.")
                input("Press Enter to continue...")
                continue
            send_json(ser, {"intent": 7, "lat": lat, "lon": lon, "speed": speed, "range": rng})
            print("GoTo command sent.")
            input("Press Enter to continue...")

        elif choice == 8:
            send_json(ser, {"intent": 8})
            print("Calibration requested (intent 8).")
            input("Press Enter to continue...")

        elif choice == 9:
            print("Start magnetometer logging — this will repeatedly request data and write to a file.")
            intent9.process(ser)
            input("Logging ended. Press Enter to continue...")

        elif choice == 10:
            try:
                biasL = float(input("Bias Left (float): "))
                biasR = float(input("Bias Right (float): "))
            except Exception:
                print("Invalid input.")
                input("Press Enter to continue...")
                continue
            send_json(ser, {"intent": 10, "biasL": biasL, "biasR": biasR})
            print("Bias command sent.")
            input("Press Enter to continue...")

        else:
            print("Unknown choice")
            input("Press Enter to continue...")


def main():
    clear()
    print("OpenMoverPlatform Helper")
    ser = None
    while ser is None:
        ser = open_serial()
        if ser is None:
            again = input("Try another port? (Y/n): ").strip().lower()
            if again == 'n':
                print("Exiting.")
                return
    try:
        menu(ser)
    finally:
        try:
            ser.close()
        except Exception:
            pass


if __name__ == '__main__':
    main()