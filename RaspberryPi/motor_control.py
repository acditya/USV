from adafruit_pca9685 import PCA9685
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
pwm = PCA9685(i2c)
pwm.frequency = 50  # ESCs use 50Hz PWM

def set_thruster_speeds(throttle, steering):
    """ Mixes throttle & steering values for 4 thrusters """
    left_power = throttle - steering
    right_power = throttle + steering

    pwm.channels[0].duty_cycle = int(left_power * 65535 / 255)
    pwm.channels[1].duty_cycle = int(right_power * 65535 / 255)
    pwm.channels[2].duty_cycle = int(left_power * 65535 / 255)
    pwm.channels[3].duty_cycle = int(right_power * 65535 / 255)
