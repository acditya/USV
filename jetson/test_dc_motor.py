import time

import RPi.GPIO as GPIO

# Pin configuration
PIN_FORWARD = 38
PIN_BACKWARD = 40

# GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_FORWARD, GPIO.OUT)
GPIO.setup(PIN_BACKWARD, GPIO.OUT)

def test_motor():
    try:
        print("Testing motor forward...")
        GPIO.output(PIN_FORWARD, GPIO.HIGH)
        GPIO.output(PIN_BACKWARD, GPIO.LOW)
        time.sleep(2)

        print("Testing motor backward...")
        GPIO.output(PIN_FORWARD, GPIO.LOW)
        GPIO.output(PIN_BACKWARD, GPIO.HIGH)
        time.sleep(2)

        print("Stopping motor...")
        GPIO.output(PIN_FORWARD, GPIO.LOW)
        GPIO.output(PIN_BACKWARD, GPIO.LOW)

    except KeyboardInterrupt:
        print("Test interrupted!")

    finally:
        GPIO.cleanup()
        print("GPIO cleaned up.")

if __name__ == "__main__":
    test_motor()