import cv2
import threading
import pyzed.sl as sl
import socket
import pickle
import struct
import logging

class VideoStream:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.running = False
        self.zed = None
        self.server_socket = None
        self.clients = []
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('VideoStream')

    def initialize_camera(self):
        """Initialize ZED camera with optimal parameters"""
        try:
            init_params = sl.InitParameters()
            init_params.camera_resolution = sl.RESOLUTION.HD720
            init_params.camera_fps = 30
            init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
            
            self.zed = sl.Camera()
            status = self.zed.open(init_params)
            
            if status != sl.ERROR_CODE.SUCCESS:
                self.logger.error(f"Camera initialization failed: {status}")
                return False
                
            return True
        except Exception as e:
            self.logger.error(f"Camera initialization error: {e}")
            return False

    def start_streaming(self):
        """Start video streaming server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            # Start client acceptance thread
            threading.Thread(target=self._accept_clients, daemon=True).start()
            
            # Start video streaming thread
            threading.Thread(target=self._stream_video, daemon=True).start()
            
            self.logger.info("Video streaming started successfully")
        except Exception as e:
            self.logger.error(f"Failed to start streaming: {e}")
            self.stop_streaming()

    def _accept_clients(self):
        """Accept new client connections"""
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                self.logger.info(f"New client connected: {addr}")
                self.clients.append(client_socket)
            except Exception as e:
                if self.running:
                    self.logger.error(f"Client acceptance error: {e}")

    def _stream_video(self):
        """Capture and stream video frames"""
        if not self.zed:
            self.logger.error("Camera not initialized")
            return

        image = sl.Mat()
        runtime_parameters = sl.RuntimeParameters()

        while self.running:
            try:
                if self.zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
                    self.zed.retrieve_image(image, sl.VIEW.LEFT)
                    frame = image.get_data()
                    
                    # Convert to jpg for efficiency
                    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                    data = pickle.dumps(buffer)
                    
                    # Send frame size followed by frame data
                    message_size = struct.pack("L", len(data))
                    
                    # Send to all connected clients
                    disconnected_clients = []
                    for client in self.clients:
                        try:
                            client.sendall(message_size + data)
                        except:
                            disconnected_clients.append(client)
                    
                    # Remove disconnected clients
                    for client in disconnected_clients:
                        self.clients.remove(client)
                        
            except Exception as e:
                self.logger.error(f"Streaming error: {e}")
                break

    def stop_streaming(self):
        """Stop video streaming and cleanup"""
        self.running = False
        
        # Close all client connections
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        self.clients.clear()
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
            
        # Close ZED camera
        if self.zed:
            self.zed.close()
            
        self.logger.info("Video streaming stopped")

    def get_depth_data(self):
        """Get depth data for autonomous navigation"""
        if not self.zed:
            return None
            
        depth = sl.Mat()
        if self.zed.grab() == sl.ERROR_CODE.SUCCESS:
            self.zed.retrieve_measure(depth, sl.MEASURE.DEPTH)
            return depth.get_data()
        return None 