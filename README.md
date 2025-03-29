# USV (Unmanned Surface Vehicle) Control System

## System Overview
This repository contains the control software for an Unmanned Surface Vehicle (USV) using a dual-computer architecture with Jetson Nano and Raspberry Pi 4. The system supports both teleoperation and autonomous navigation modes.

### Key Features
- Dual-computer architecture for distributed processing
- Real-time video streaming with depth sensing
- Robust RC control with failsafes
- Autonomous navigation capabilities
- Gate control mechanism
- Differential drive thrust mixing
- Comprehensive error handling and logging
- Clean shutdown procedures

### Hardware Components
- **Jetson Nano**: Main control computer, handles video processing and high-level control
- **Raspberry Pi 4**: Hardware interface computer, manages motors and sensors
- **ZED Camera**: Stereoscopic camera for depth sensing and navigation
- **FlySky FS-i6X**: RC transmitter with iA10B receiver
- **4x T200 Thrusters**: Main propulsion
- **Gate Mechanism**: DC motor with limit switches
- **PCA9685**: 16-channel PWM controller for thrusters
- **Power System**: Independent power supplies for computers and motors

## Software Architecture

### Jetson Nano Components
1. **main.py**
   - System initialization and main control loop
   - Mode switching between autonomous and teleoperation
   - Video stream management

2. **teleoperation/**
   - **video_stream.py**: ZED camera interface and video streaming
   - **command_processor.py**: RC input processing and command generation

3. **utils/**
   - **communication.py**: I2C communication with Raspberry Pi

### Raspberry Pi Components
1. **main.py**
   - Hardware control loop
   - Command processing from Jetson Nano
   - Safety monitoring and failsafes

2. **controllers/**
   - **motor_controller.py**: Thruster control and mixing
   - **gate_controller.py**: Gate mechanism control
   - **receiver_controller.py**: RC receiver interface

## Setup Instructions

### 1. Dependencies Installation
```bash
# On both computers
pip install -r requirements.txt

# Additional Jetson Nano setup
apt-get install python3-smbus
```

### 2. Hardware Configuration
1. **Raspberry Pi Setup**
   ```bash
   # Enable I2C and Serial
   sudo raspi-config
   # Select: Interface Options -> I2C -> Yes
   # Select: Interface Options -> Serial -> Yes
   ```

2. **Jetson Nano Setup**
   ```bash
   # Install ZED SDK from stereolabs.com
   ./ZED_SDK_Linux_JetsonNano.run
   ```

### 3. Network Configuration
1. Configure static IPs:
   - Jetson Nano: 192.168.1.10
   - Raspberry Pi: 192.168.1.11

2. Enable SSH on both devices

### 4. System Startup
1. **On Raspberry Pi**:
   ```bash
   cd raspberry_pi
   python3 main.py
   ```

2. **On Jetson Nano**:
   ```bash
   cd jetson
   python3 main.py
   ```

## Control Modes

### 1. Teleoperation Mode
- Right stick: Throttle control
- Left stick: Steering control
- Switch A: Mode selection (Manual/Auto)
- Switch B: Emergency stop
- Switch C: Gate control

### 2. Autonomous Mode
- Activated via Switch A
- Uses ZED camera for navigation
- Automatic obstacle avoidance
- Can be overridden by RC input

## Safety Features
- Command timeout failsafe
- Emergency stop procedure
- Motor acceleration limiting
- Gate operation timeout
- Signal quality monitoring
- Clean shutdown handling

## Troubleshooting

### Common Issues
1. **No RC Control**
   - Check receiver connections
   - Verify channel mappings
   - Check signal quality

2. **Motor Issues**
   - Verify ESC calibration
   - Check PWM signals
   - Verify power supply

3. **Camera Problems**
   - Check ZED SDK installation
   - Verify USB connection
   - Check streaming port availability

## Development

### Adding New Features
1. Create feature branch
2. Implement changes
3. Test thoroughly
4. Submit pull request

### Code Style
- Follow PEP 8
- Use comprehensive error handling
- Maintain logging consistency
- Document all functions

## License
MIT License

## Contributors
[Your Name]
