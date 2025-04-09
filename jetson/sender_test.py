# jetson_sender.py
import serial

# Configure the serial connection
serial_port = '/dev/ttyUSB0'  # Replace with the correct port
baud_rate = 9600

try:
    ser = serial.Serial(serial_port, baud_rate)
    print(f"Connected to {serial_port} at {baud_rate} baud.")
    while True:
        # Read input from the user
        data = input("Enter a message to send: ")
        ser.write(data.encode('utf-8'))  # Send data over serial
except serial.SerialException as e:
    print(f"Serial error: {e}")
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()