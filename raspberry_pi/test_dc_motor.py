import time
import RPi.GPIO as GPIO

# Set up GPIO mode
GPIO.setmode(GPIO.BOARD)

# Define GPIO pins
ENA = 37  # PWM pin for speed control
IN1 = 38  # Direction pin 1
IN2 = 40  # Direction pin 2

# Set up the GPIO pins
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

# Set up PWM on ENA
pwm = GPIO.PWM(ENA, 100)  # 100 Hz frequency
pwm.start(0)  # Start with 0% duty cycle (motor off)

try:
    # Spin the motor forward at 50% speed
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(50)
    print("Motor spinning forward at 50% speed")
    time.sleep(2)

    # Spin the motor backward at 75% speed
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(75)
    print("Motor spinning backward at 75% speed")
    time.sleep(2)

    # Stop the motor
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)
    print("Motor stopped")

finally:
    # Clean up GPIO settings
    pwm.stop()
    GPIO.cleanup()
    print("GPIO cleanup done")
