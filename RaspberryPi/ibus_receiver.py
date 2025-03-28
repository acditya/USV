import serial

ser = serial.Serial("/dev/serial0", 115200, timeout=1)

def read_ibus():
    """ Reads iBUS data from FlySky receiver """
    if ser.in_waiting > 32:
        data = ser.read(32)
        channels = [int.from_bytes(data[i:i+2], "little") for i in range(2, 30, 2)]
        return channels
    return None

while True:
    channels = read_ibus()
    if channels:
        print(f"Throttle: {channels[2]}, Steering: {channels[0]}, Gate: {channels[6]}")
