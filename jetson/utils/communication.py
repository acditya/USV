import smbus
import logging
from time import sleep

class I2CCommunicator:
    def __init__(self, address=0x08, bus_number=1):
        self.address = address
        self.bus_number = bus_number
        self.logger = logging.getLogger('I2CCommunicator')
        
        try:
            self.bus = smbus.SMBus(bus_number)
        except Exception as e:
            self.logger.error(f"Failed to initialize I2C: {e}")
            self.bus = None
            
        # Command retry parameters
        self.max_retries = 3
        self.retry_delay = 0.1
            
    def send_command(self, throttle, steering, gate_control):
        """
        Send command to Raspberry Pi with retry mechanism
        """
        if not self.bus:
            self.logger.error("I2C bus not initialized")
            return False
            
        data = [throttle, steering, gate_control]
        
        for attempt in range(self.max_retries):
            try:
                self.bus.write_i2c_block_data(self.address, 0, data)
                return True
            except Exception as e:
                self.logger.warning(f"I2C write attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    sleep(self.retry_delay)
                    
        self.logger.error("Failed to send command after all retries")
        return False
        
    def read_response(self):
        """
        Read response from Raspberry Pi
        """
        if not self.bus:
            return None
            
        try:
            return self.bus.read_i2c_block_data(self.address, 0, 3)
        except Exception as e:
            self.logger.error(f"Failed to read I2C response: {e}")
            return None 