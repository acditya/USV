import RPi.GPIO as GPIO
import time

MOTOR_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

def control_gate(command):
    """ Controls gate motor based on command: 1 = Open, 2 = Close """
    if command == 1:
        GPIO.output(MOTOR_PIN, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(MOTOR_PIN, GPIO.LOW)
    elif command == 2:
        GPIO.output(MOTOR_PIN, GPIO.LOW)
