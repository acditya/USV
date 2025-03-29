import serial
import logging
from threading import Thread, Lock
import time

class ReceiverController:
    def __init__(self, port="/dev/serial0", baudrate=115200):
        self.logger = logging.getLogger('ReceiverController')
        
        # Serial configuration
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        
        # Channel configuration
        self.channel_map = {
            'steering': 0,    # Right stick X
            'throttle': 2,    # Left stick Y
            'aux1': 4,       # Switch A
            'aux2': 5,       # Switch B
            'gate': 6        # Switch C
        }
        
        # Data handling
        self.channels = [1500] * 14  # Default to center position
        self.data_lock = Lock()
        self.running = False
        
        # Signal quality monitoring
        self.last_update = 0
        self.signal_timeout = 0.5  # 500ms timeout
        
        self._initialize_serial()
        
    def _initialize_serial(self):
        """Initialize serial connection to receiver"""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=0.1
            )
            self.running = True
            
            # Start reading thread
            Thread(target=self._read_loop, daemon=True).start()
            
            self.logger.info("RC receiver initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize RC receiver: {e}")
            return False
            
    def _read_loop(self):
        """Continuous reading loop for iBUS data"""
        while self.running:
            try:
                if self.serial.in_waiting > 32:
                    data = self.serial.read(32)
                    
                    # Verify iBUS protocol header
                    if data[0] == 0x20 and data[1] == 0x40:
                        with self.data_lock:
                            # Parse channel data
                            for i in range(14):
                                self.channels[i] = int.from_bytes(
                                    data[2+2*i:4+2*i], 
                                    byteorder='little'
                                )
                            self.last_update = time.time()
                            
            except Exception as e:
                self.logger.error(f"Error reading RC data: {e}")
                time.sleep(0.1)
                
    def read_channels(self):
        """
        Read current channel values
        Returns dict of channel values mapped to functions
        """
        if not self.running:
            return None
            
        # Check signal timeout
        if time.time() - self.last_update > self.signal_timeout:
            self.logger.warning("RC signal timeout")
            return None
            
        with self.data_lock:
            try:
                return {
                    name: self._normalize_channel(self.channels[channel])
                    for name, channel in self.channel_map.items()
                }
            except Exception as e:
                self.logger.error(f"Error processing channel data: {e}")
                return None
                
    def _normalize_channel(self, value):
        """
        Normalize channel value to 0-255 range
        Handles common RC values (1000-2000)
        """
        # Clamp input range
        value = max(1000, min(2000, value))
        
        # Convert to 0-255 range
        return int(((value - 1000) * 255) / 1000)
        
    def close(self):
        """Clean shutdown of receiver"""
        self.running = False
        if self.serial:
            try:
                self.serial.close()
            except:
                pass 