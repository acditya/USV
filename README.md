# USV Control System (Jetson Nano & Raspberry Pi 4)

## Overview
This project sets up a **Jetson Nano (Master)** and **Raspberry Pi 4 (Slave)** to control a **Unmanned Surface Vehicle (USV)** powered by **four Blue Robotics T200 thrusters (ESC-driven)** and a **gate mechanism (DC motor-driven)**. The system is controlled using an **FS-i6X RC transmitter** paired with an **iA10B receiver**.

## Table of Contents
- [Hardware Requirements](#hardware-requirements)
- [Connections & Pin Mapping](#connections--pin-mapping)
- [FS-i6X Input Mapping](#fs-i6x-input-mapping)
- [Software Setup](#software-setup)
- [Code Structure](#code-structure)
- [Running the System](#running-the-system)
- [Troubleshooting](#troubleshooting)

---
## Hardware Requirements
### **Main Components**
- **Jetson Nano** (Master) – AI processing & command relay
- **Raspberry Pi 4** (Slave) – Motor controller
- **FS-i6X RC Transmitter** – User control
- **FlySky iA10B Receiver** – Wireless signal reception
- **4x Blue Robotics T200 Thrusters** – Propulsion
- **4x ESCs (Electronic Speed Controllers)** – Motor control
- **1x Motor Driver** – Gate mechanism control
- **5V & 12V Power Supplies**
- **Jumper Wires, Dupont Connectors, and Breadboards**

---
## Connections & Pin Mapping
### **FS-i6X Receiver (iA10B) to Raspberry Pi 4**
| Receiver Channel | Function | Raspberry Pi GPIO |
|-----------------|-------------------|-----------------|
| CH1 | Right Joystick X (Yaw) | GPIO 17 |
| CH2 | Right Joystick Y (Throttle) | GPIO 27 |
| CH5 | Switch A (Gate Control) | GPIO 22 |

### **ESC Connections to Raspberry Pi 4**
| Thruster | ESC PWM Signal | Power |
|----------|----------------|--------|
| Front Left | GPIO 18 | 12V |
| Front Right | GPIO 23 | 12V |
| Rear Left | GPIO 24 | 12V |
| Rear Right | GPIO 25 | 12V |

### **Motor Driver for Gate Mechanism**
| Motor Function | Motor Driver Input | Raspberry Pi GPIO |
|---------------|-----------------|-----------------|
| Open Gate | IN1 | GPIO 5 |
| Close Gate | IN2 | GPIO 6 |

---
## FS-i6X Input Mapping
### **Joystick Mapping**
- **Right Joystick (CH1 & CH2):** Controls USV movement (Yaw & Throttle)
- **Switch A (CH5):** Toggles the gate mechanism

### **PWM Signal Scaling**
The **FS-i6X receiver outputs PWM signals** that will be read using the Raspberry Pi. The values range from **1000µs to 2000µs** and will be mapped accordingly to motor power levels.

---
## Software Setup
### **Jetson Nano (Master)**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip -y
pip3 install paramiko
```

### **Raspberry Pi 4 (Slave)**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip pigpio -y
pip3 install gpiozero
```

### **Enable `pigpio` daemon for PWM control**
```bash
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
```

---
## Code Structure
```
USV-Control-System/
├── jetson_nano/   # Master Node
│   ├── master.py  # Sends commands to RPi
│   ├── config.py  # IP & SSH settings
│   └── utils.py   # Helper functions
│
├── raspberry_pi/  # Slave Node
│   ├── slave.py   # Reads PWM & controls motors
│   ├── esc_control.py  # ESC driver
│   ├── motor_driver.py  # Gate mechanism
│   ├── receiver.py  # FS-i6X PWM Reader
│   └── utils.py   # Helper functions
│
└── README.md      # This File
```

---
## Running the System
### **Step 1: Start Raspberry Pi (Slave)**
```bash
cd raspberry_pi/
python3 slave.py
```

### **Step 2: Start Jetson Nano (Master)**
```bash
cd jetson_nano/
python3 master.py
```

---
## Troubleshooting
- **Issue: ESCs are not responding**
  - Ensure `pigpiod` is running: `sudo systemctl start pigpiod`
  - Check GPIO connections
  - Verify power supply to ESCs

- **Issue: No response from FS-i6X Receiver**
  - Check PWM signal with an oscilloscope
  - Ensure correct GPIO pins are used

- **Issue: Connection failure between Jetson & Pi**
  - Test SSH connectivity: `ssh pi@<raspberry_pi_ip>`
  - Ensure correct IP settings in `config.py`

---
## Next Steps
- Implement advanced **PID control** for thrusters
- Add **IMU integration** for stability
- Extend to **autonomous waypoint navigation**

---
## Author
**Aditya Chatterjee** 🚀
