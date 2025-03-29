import numpy as np
import logging
from ..utils.communication import I2CCommunicator

class CommandProcessor:
    def __init__(self):
        self.i2c_comm = I2CCommunicator()
        self.logger = logging.getLogger('CommandProcessor')
        
        # Control parameters
        self.max_speed = 255
        self.dead_zone = 0.05  # 5% deadzone for joystick
        self.smoothing_factor = 0.3  # For exponential smoothing
        
        # State variables
        self.last_throttle = 0
        self.last_steering = 0
        
    def process_rc_input(self, channels):
        """
        Process RC receiver channels and convert to motor commands
        channels: List of channel values (typically 1000-2000)
        """
        try:
            # Extract and normalize joystick values (-1 to 1)
            throttle = self._normalize_rc(channels[2])  # Channel 3
            steering = self._normalize_rc(channels[0])  # Channel 1
            gate_command = self._process_gate_input(channels[6])  # Channel 7
            
            # Apply deadzone
            throttle = self._apply_deadzone(throttle)
            steering = self._apply_deadzone(steering)
            
            # Apply exponential smoothing
            throttle = self._smooth_value(throttle, self.last_throttle)
            steering = self._smooth_value(steering, self.last_steering)
            
            # Convert to motor commands (0-255)
            throttle_cmd = self._to_motor_command(throttle)
            steering_cmd = self._to_motor_command(steering)
            
            # Update last values
            self.last_throttle = throttle
            self.last_steering = steering
            
            # Send commands to Raspberry Pi
            self.i2c_comm.send_command(throttle_cmd, steering_cmd, gate_command)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing RC input: {e}")
            return False
            
    def _normalize_rc(self, value):
        """Convert RC value (1000-2000) to normalized (-1 to 1)"""
        return (value - 1500) / 500
        
    def _apply_deadzone(self, value):
        """Apply deadzone to prevent motor jitter"""
        if abs(value) < self.dead_zone:
            return 0
        return value
        
    def _smooth_value(self, current, last):
        """Apply exponential smoothing"""
        return last + self.smoothing_factor * (current - last)
        
    def _to_motor_command(self, value):
        """Convert normalized value to motor command (0-255)"""
        return int(((value + 1) / 2) * self.max_speed)
        
    def _process_gate_input(self, gate_channel):
        """Process gate control channel"""
        if gate_channel > 1800:  # Open gate
            return 1
        elif gate_channel < 1200:  # Close gate
            return 2
        return 0  # No change
        
    def move(self, direction, speed=0.5):
        """
        High-level movement command
        direction: 'forward', 'backward', 'left', 'right'
        speed: 0.0 to 1.0
        """
        speed = max(0.0, min(1.0, speed))  # Clamp speed
        
        commands = {
            'forward': (speed, 0),
            'backward': (-speed, 0),
            'left': (0, -speed),
            'right': (0, speed),
        }
        
        if direction in commands:
            throttle, steering = commands[direction]
            throttle_cmd = self._to_motor_command(throttle)
            steering_cmd = self._to_motor_command(steering)
            self.i2c_comm.send_command(throttle_cmd, steering_cmd, 0)
            return True
        return False
        
    def stop(self):
        """Emergency stop command"""
        self.i2c_comm.send_command(128, 128, 0)  # Neutral position
        self.last_throttle = 0
        self.last_steering = 0 