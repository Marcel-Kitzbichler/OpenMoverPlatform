import serial

# Configure the serial port
ser = serial.Serial(
    port=input("Bot Serial Port? :"),        # Replace with your port name
    baudrate=115200,      # Set the baud rate
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1           # Set a timeout value
)

if ser.is_open:
    print("0: upload cords")
    print("1: download cords")
    print("2: start wp mission")
    choice = int(input("Choice :"))

    if choice == 0:

    elif choice == 1:

    elif choice == 2: