# raspberry_receiver.py
import serial

# Configure the serial connection
serial_port = '/dev/ttyUSB0'  # Replace with the correct port
baud_rate = 9600

try:
    ser = serial.Serial(serial_port, baud_rate)
    print(f"Listening on {serial_port} at {baud_rate} baud.")
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()  # Read and decode data
            print(f"Received: {data}")
except serial.SerialException as e:
    print(f"Serial error: {e}")
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()