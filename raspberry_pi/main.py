import logging
import signal
import sys
from controllers.motor_controller import MotorController
from controllers.gate_controller import GateController
from controllers.receiver_controller import ReceiverController
import time

class USVHardwareController:
    def __init__(self):
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('USVHardwareController')
        
        # Initialize controllers
        self.motor_controller = MotorController()
        self.gate_controller = GateController()
        self.receiver = ReceiverController()
        
        # Control flags
        self.running = False
        self.direct_rc_mode = False  # For direct RC control bypass
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Watchdog timer for command timeout
        self.last_command_time = time.time()
        self.command_timeout = 1.0  # 1 second timeout
        
    def start(self):
        """Initialize and start the hardware control system"""
        self.logger.info("Starting USV Hardware Control System...")
        
        # Calibrate ESCs
        if not self.motor_controller.calibrate_escs():
            self.logger.error("ESC calibration failed. Please check connections.")
            return False
            
        self.running = True
        
        try:
            self._main_loop()
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}")
            self.shutdown()
            
    def _main_loop(self):
        """Main control loop"""
        while self.running:
            try:
                current_time = time.time()
                
                # Check for direct RC control
                rc_data = self.receiver.read_channels()
                if rc_data:
                    self.direct_rc_mode = rc_data.get('aux1', False)  # Aux channel for mode selection
                    
                if self.direct_rc_mode:
                    # Direct RC control mode
                    self._handle_rc_control(rc_data)
                else:
                    # Normal I2C command mode
                    self._handle_i2c_commands()
                    
                # Check command timeout
                if current_time - self.last_command_time > self.command_timeout:
                    self.logger.warning("Command timeout - engaging safety stop")
                    self.motor_controller.emergency_stop()
                    
                time.sleep(0.01)  # 100Hz update rate
                
            except Exception as e:
                self.logger.error(f"Error in control loop: {e}")
                self.motor_controller.emergency_stop()
                
    def _handle_rc_control(self, rc_data):
        """Process direct RC control inputs"""
        if not rc_data:
            return
            
        try:
            # Update last command time
            self.last_command_time = time.time()
            
            # Process RC channels
            throttle = rc_data.get('throttle', 128)
            steering = rc_data.get('steering', 128)
            gate = rc_data.get('gate', 0)
            
            # Apply commands
            self.motor_controller.set_thruster_speeds(throttle, steering)
            self.gate_controller.control_gate(gate)
            
        except Exception as e:
            self.logger.error(f"Error processing RC control: {e}")
            self.motor_controller.emergency_stop()
            
    def _handle_i2c_commands(self):
        """Process commands from Jetson Nano via I2C"""
        try:
            # Read I2C commands (implement this based on your I2C setup)
            commands = self._read_i2c_commands()
            
            if commands:
                throttle, steering, gate = commands
                self.last_command_time = time.time()
                
                # Apply commands
                self.motor_controller.set_thruster_speeds(throttle, steering)
                self.gate_controller.control_gate(gate)
                
        except Exception as e:
            self.logger.error(f"Error processing I2C commands: {e}")
            self.motor_controller.emergency_stop()
            
    def _read_i2c_commands(self):
        """Read commands from I2C bus"""
        # Implement I2C reading logic here
        return None
            
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info("Shutdown signal received")
        self.shutdown()
        
    def shutdown(self):
        """Clean shutdown of all systems"""
        self.logger.info("Shutting down USV Hardware Control System...")
        self.running = False
        self.motor_controller.emergency_stop()
        self.gate_controller.close()  # Implement this in gate controller
        sys.exit(0)

if __name__ == "__main__":
    controller = USVHardwareController()
    controller.start() 