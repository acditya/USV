import RPi.GPIO as GPIO
import logging
import time
from threading import Lock

class GateController:
    def __init__(self, motor_pin=18, limit_switch_open=23, limit_switch_closed=24):
        self.logger = logging.getLogger('GateController')
        
        # Pin configuration
        self.motor_pin = motor_pin
        self.limit_switch_open = limit_switch_open
        self.limit_switch_closed = limit_switch_closed
        
        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_pin, GPIO.OUT)
        GPIO.setup(self.limit_switch_open, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.limit_switch_closed, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Create PWM object for motor control
        self.motor_pwm = GPIO.PWM(self.motor_pin, 100)  # 100Hz PWM frequency
        self.motor_pwm.start(0)
        
        # State tracking
        self.current_state = "unknown"  # unknown, opening, closing, open, closed
        self.last_command = 0
        self.command_lock = Lock()
        
        # Timing parameters
        self.max_operation_time = 5.0  # Maximum time for open/close operation
        self.operation_start_time = 0
        
    def control_gate(self, command):
        """
        Control gate based on command
        command: 0 = Stop, 1 = Open, 2 = Close
        """
        with self.command_lock:
            try:
                if command == self.last_command:
                    return
                    
                self.last_command = command
                
                if command == 1:  # Open
                    self._open_gate()
                elif command == 2:  # Close
                    self._close_gate()
                else:  # Stop
                    self._stop_gate()
                    
            except Exception as e:
                self.logger.error(f"Gate control error: {e}")
                self._stop_gate()
                
    def _open_gate(self):
        """Open the gate"""
        if self._is_fully_open():
            self._stop_gate()
            return
            
        self.current_state = "opening"
        self.operation_start_time = time.time()
        self.motor_pwm.ChangeDutyCycle(100)  # Full power to open
        
    def _close_gate(self):
        """Close the gate"""
        if self._is_fully_closed():
            self._stop_gate()
            return
            
        self.current_state = "closing"
        self.operation_start_time = time.time()
        self.motor_pwm.ChangeDutyCycle(-100)  # Full power to close
        
    def _stop_gate(self):
        """Stop gate movement"""
        self.motor_pwm.ChangeDutyCycle(0)
        self.current_state = "stopped"
        
    def _is_fully_open(self):
        """Check if gate is fully open"""
        return not GPIO.input(self.limit_switch_open)
        
    def _is_fully_closed(self):
        """Check if gate is fully closed"""
        return not GPIO.input(self.limit_switch_closed)
        
    def _check_timeout(self):
        """Check if operation has timed out"""
        if self.current_state in ["opening", "closing"]:
            if time.time() - self.operation_start_time > self.max_operation_time:
                self.logger.warning("Gate operation timed out")
                self._stop_gate()
                return True
        return False
        
    def get_state(self):
        """Get current gate state"""
        if self._is_fully_open():
            return "open"
        elif self._is_fully_closed():
            return "closed"
        else:
            return self.current_state
            
    def close(self):
        """Cleanup GPIO"""
        self.motor_pwm.stop()
        GPIO.cleanup([self.motor_pin, self.limit_switch_open, self.limit_switch_closed]) 