import smbus
import time
from motor_control import set_thruster_speeds
from gate_control import control_gate

I2C_ADDR = 0x08
bus = smbus.SMBus(1)

def receive_i2c_command():
    """ Receives motor and gate commands from Jetson Nano """
    try:
        data = bus.read_i2c_block_data(I2C_ADDR, 0, 3)
        throttle, steering, gate_control = data
        return throttle, steering, gate_control
    except Exception as e:
        print("I2C Read Error:", e)
        return None, None, None

while True:
    throttle, steering, gate_control = receive_i2c_command()
    
    if throttle is not None:
        set_thruster_speeds(throttle, steering)
        control_gate(gate_control)

    time.sleep(0.1)
