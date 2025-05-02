import serial
import intent5
import intent1
import intent2
import os

# Configure the serial port
ser = serial.Serial(
    port=input("Bot Serial Port? :"),        # Replace with your port name
    baudrate=115200,      # Set the baud rate
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1           # Set a timeout value
)


while True:
    if ser.is_open:
        os.system('cls')
        print("0: upload cords")
        print("1: download cords")
        print("2: start wp mission")
        choice = int(input("Choice :"))

        if choice == 0:
            intent5.process(ser)

        elif choice == 1:
            intent1.process(ser)

        elif choice == 2:
            intent2.process(ser)