import logging
import signal
import sys
from teleoperation.command_processor import CommandProcessor
from teleoperation.video_stream import VideoStream
import time

class USVController:
    def __init__(self):
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('USVController')
        
        # Initialize components
        self.command_processor = CommandProcessor()
        self.video_stream = VideoStream()
        
        # Control flags
        self.running = False
        self.autonomous_mode = False
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def start(self):
        """Initialize and start the USV control system"""
        self.logger.info("Starting USV Control System...")
        
        # Initialize video streaming
        if not self.video_stream.initialize_camera():
            self.logger.error("Failed to initialize camera. Exiting.")
            return False
            
        self.video_stream.start_streaming()
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
                # Check mode switch status (implement this based on your mode switch input)
                self.autonomous_mode = self._check_mode_switch()
                
                if self.autonomous_mode:
                    self._run_autonomous_mode()
                else:
                    self._run_teleoperation_mode()
                    
                time.sleep(0.01)  # 100Hz update rate
                
            except Exception as e:
                self.logger.error(f"Error in control loop: {e}")
                
    def _run_teleoperation_mode(self):
        """Handle teleoperation mode"""
        # Process RC commands (implement RC reading logic)
        throttle = 128  # Replace with actual RC reading
        steering = 128  # Replace with actual RC reading
        gate = 0       # Replace with actual RC reading
        
        self.command_processor.process_rc_input([0, 0, throttle, 0, 0, 0, gate])
        
    def _run_autonomous_mode(self):
        """Handle autonomous mode"""
        # Get depth data for navigation
        depth_data = self.video_stream.get_depth_data()
        if depth_data is not None:
            # Implement autonomous navigation logic here
            # This is where you would add your ML-based navigation
            pass
            
    def _check_mode_switch(self):
        """Check the mode switch status"""
        # Implement mode switch checking logic
        # This could be from an RC channel or other input
        return False  # Default to manual mode
        
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info("Shutdown signal received")
        self.shutdown()
        
    def shutdown(self):
        """Clean shutdown of all systems"""
        self.logger.info("Shutting down USV Control System...")
        self.running = False
        self.video_stream.stop_streaming()
        # Add any other cleanup needed
        sys.exit(0)

if __name__ == "__main__":
    controller = USVController()
    controller.start() 