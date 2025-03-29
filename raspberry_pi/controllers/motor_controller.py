from adafruit_pca9685 import PCA9685
import board
import busio
import logging
import numpy as np
from time import sleep

class MotorController:
    def __init__(self):
        self.logger = logging.getLogger('MotorController')
        
        # Initialize I2C and PCA9685
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.pwm = PCA9685(i2c)
            self.pwm.frequency = 50
            self.initialized = True
        except Exception as e:
            self.logger.error(f"Failed to initialize PCA9685: {e}")
            self.initialized = False
            
        # Motor configuration
        self.motor_channels = {
            'front_left': 0,
            'front_right': 1,
            'rear_left': 2,
            'rear_right': 3
        }
        
        # Control parameters
        self.min_pulse = 1100
        self.max_pulse = 1900
        self.neutral_pulse = 1500
        
        # Safety features
        self.emergency_stop_active = False
        self.max_acceleration = 0.2  # Maximum change in power per update
        self.current_powers = {channel: 0 for channel in self.motor_channels.values()}
        
    def set_thruster_speeds(self, throttle, steering):
        """
        Set thruster speeds based on throttle and steering inputs
        throttle: 0-255 (128 is neutral)
        steering: 0-255 (128 is neutral)
        """
        if not self.initialized or self.emergency_stop_active:
            return False
            
        try:
            # Normalize inputs to -1 to 1
            throttle = (throttle - 128) / 128
            steering = (steering - 128) / 128
            
            # Calculate motor powers using mixing algorithm
            powers = self._mix_powers(throttle, steering)
            
            # Apply power to each motor with acceleration limiting
            for motor, power in powers.items():
                channel = self.motor_channels[motor]
                limited_power = self._limit_acceleration(channel, power)
                self._set_motor_power(channel, limited_power)
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting thruster speeds: {e}")
            self.emergency_stop()
            return False
            
    def _mix_powers(self, throttle, steering):
        """
        Mix throttle and steering commands for differential drive
        Returns dict of motor powers (-1 to 1)
        """
        left_power = throttle - steering
        right_power = throttle + steering
        
        # Normalize if any power exceeds [-1, 1]
        max_power = max(abs(left_power), abs(right_power))
        if max_power > 1:
            left_power /= max_power
            right_power /= max_power
            
        return {
            'front_left': left_power,
            'front_right': right_power,
            'rear_left': left_power,
            'rear_right': right_power
        }
        
    def _limit_acceleration(self, channel, target_power):
        """Limit acceleration to prevent sudden changes"""
        current_power = self.current_powers[channel]
        power_change = target_power - current_power
        
        if abs(power_change) > self.max_acceleration:
            power_change = np.sign(power_change) * self.max_acceleration
            
        new_power = current_power + power_change
        self.current_powers[channel] = new_power
        return new_power
        
    def _set_motor_power(self, channel, power):
        """
        Set motor power (-1 to 1) for given channel
        Converts power to appropriate PWM pulse width
        """
        # Convert power to pulse width
        pulse_range = self.max_pulse - self.min_pulse
        pulse_width = self.neutral_pulse + (power * pulse_range / 2)
        
        # Convert pulse width to duty cycle
        duty_cycle = int((pulse_width / 20000) * 65535)
        
        # Set PWM
        self.pwm.channels[channel].duty_cycle = duty_cycle
        
    def emergency_stop(self):
        """Emergency stop all motors"""
        self.emergency_stop_active = True
        if self.initialized:
            for channel in self.motor_channels.values():
                self.pwm.channels[channel].duty_cycle = int((self.neutral_pulse / 20000) * 65535)
                self.current_powers[channel] = 0
                
    def resume(self):
        """Resume normal operation after emergency stop"""
        self.emergency_stop_active = False
        
    def calibrate_escs(self):
        """Calibrate ESCs"""
        if not self.initialized:
            return False
            
        try:
            # Set max pulse
            for channel in self.motor_channels.values():
                self.pwm.channels[channel].duty_cycle = int((self.max_pulse / 20000) * 65535)
            sleep(2)
            
            # Set min pulse
            for channel in self.motor_channels.values():
                self.pwm.channels[channel].duty_cycle = int((self.min_pulse / 20000) * 65535)
            sleep(2)
            
            # Set neutral
            for channel in self.motor_channels.values():
                self.pwm.channels[channel].duty_cycle = int((self.neutral_pulse / 20000) * 65535)
            sleep(2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"ESC calibration failed: {e}")
            return False 