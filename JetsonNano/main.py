import smbus
import time

I2C_ADDR = 0x08  # I2C address of Raspberry Pi

bus = smbus.SMBus(1)  # I2C Channel 1

def send_motor_command(throttle, steering, gate_control):
    """ Sends throttle, steering, and gate control commands over I2C """
    data = [throttle, steering, gate_control]
    bus.write_i2c_block_data(I2C_ADDR, 0, data)
    print(f"Sent command: Throttle={throttle}, Steering={steering}, Gate={gate_control}")

while True:
    throttle = 128  # Placeholder (0-255)
    steering = 128  # Placeholder (0-255)
    gate_control = 0  # 0 = No change, 1 = Open, 2 = Close

    send_motor_command(throttle, steering, gate_control)
    time.sleep(0.1)
