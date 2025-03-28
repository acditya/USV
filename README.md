# USV Control System - Jetson Nano & Raspberry Pi 4

## Overview
This repository contains all necessary code to operate an **Unmanned Surface Vehicle (USV)** using:
- **Jetson Nano** (Master)
- **Raspberry Pi 4** (Slave - Motor Control)
- **FlySky FS-i6X RC Controller** (for manual control via iA10B Receiver)
- **4 Blue Robotics T200 Thrusters** (via ESCs)
- **1 DC Motor** (for opening/closing a gate)
- **Stereolabs ZED Camera** (for computer vision & autonomy)
- **TP-Link TL-MR3020 Router** (for remote access & control over Wi-Fi)

This system allows the USV to operate in two modes:
1. **Teleoperated Track** (Manual) - Control via RC controller with live video feedback.
2. **Autonomous Track** - Object detection & navigation using the **Stereolabs ZED Camera**.

---

## Hardware Setup
### 1. Wiring the Raspberry Pi 4 (Slave) to Motors & ESCs
#### **ESC Connections (Thrusters)**
| Thruster | ESC Signal Pin | Power Source |
|----------|---------------|--------------|
| Left Front (LF) | GPIO 17 (Pin 11) | LiPo Battery |
| Right Front (RF) | GPIO 27 (Pin 13) | LiPo Battery |
| Left Back (LB) | GPIO 22 (Pin 15) | LiPo Battery |
| Right Back (RB) | GPIO 23 (Pin 16) | LiPo Battery |

#### **DC Motor (Gate Mechanism) Connections**
| Function | Motor Driver Pin | Raspberry Pi GPIO |
|----------|-----------------|-------------------|
| Open Gate | IN1 | GPIO 5 (Pin 29) |
| Close Gate | IN2 | GPIO 6 (Pin 31) |
| PWM Control | ENA | GPIO 12 (Pin 32) |

#### **FlySky iA10B Receiver Connections**
| Channel | Function | Connected To |
|---------|----------|--------------|
| CH1 | Right Joystick X (Steering) | Raspberry Pi GPIO 18 (PWM) |
| CH2 | Right Joystick Y (Throttle) | Raspberry Pi GPIO 19 (PWM) |
| CH5 | Mode Switch (Manual/Auto) | Raspberry Pi GPIO 26 |

---

## Software Setup
### 2. Flashing Raspberry Pi OS (Fresh Install)
1. Download **Raspberry Pi OS (64-bit)** from the official [Raspberry Pi website](https://www.raspberrypi.org/software/operating-systems/).
2. Use **Raspberry Pi Imager** or **balenaEtcher** to flash the OS onto a microSD card.
3. Create an **SSH file** in the boot directory to enable remote access:
   ```sh
   touch /boot/ssh
   ```
4. Insert the microSD card into the **Raspberry Pi** and power it up.

### 3. Setting Up Wi-Fi & SSH with TP-Link TL-MR3020
#### **Configuring the Router (TL-MR3020)**
1. Connect to the router via **Ethernet or Wi-Fi**.
2. Open a browser and go to `192.168.0.1` (default gateway).
3. Login (default credentials: `admin/admin`).
4. Set **Wi-Fi SSID & Password** for the Jetson Nano & Raspberry Pi to connect.
5. Save and restart the router.

#### **Connecting Jetson Nano & Raspberry Pi to the Router**
On **Jetson Nano**:
```sh
nmcli device wifi connect "Your_SSID" password "Your_Password"
```
On **Raspberry Pi**:
```sh
echo -e "network={\n ssid=\"Your_SSID\"\n psk=\"Your_Password\"\n}" | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf
sudo reboot
```

#### **Finding Device IPs & Enabling SSH**
Once connected, find the IP addresses:
```sh
arp -a
```
Use SSH to access the devices:
```sh
ssh pi@<Raspberry_Pi_IP>
ssh jetson@<Jetson_Nano_IP>
```
---

## 4. Running the USV System
### **Starting Teleoperation Mode** (RC Controller → Jetson Nano → Raspberry Pi → Motors)
1. Power on **RC Controller & iA10B Receiver**.
2. Start the **Raspberry Pi Motor Control Script**:
   ```sh
   python3 motor_control.py
   ```
3. Start the **Jetson Nano Command Processing Script**:
   ```sh
   python3 nano_master.py
   ```
4. Observe the **thruster response** via the controller.

### **Switching to Autonomous Mode** (ZED Camera → Object Detection → Motor Commands)
1. Enable **autonomy mode** via the RC **Mode Switch (CH5)**.
2. Run **object detection & pathfinding** on the Jetson Nano:
   ```sh
   python3 autonomy.py
   ```
3. The system will navigate obstacles automatically.

---

## 5. Troubleshooting & Debugging
| Issue | Solution |
|--------|-----------|
| ESCs not responding | Check wiring & ESC calibration. Ensure correct PWM signal pins. |
| SSH not working | Verify IP addresses with `arp -a` and restart the router. |
| No video stream | Ensure the ZED Camera is detected using `lsusb`. Restart `autonomy.py`. |

---

## Future Improvements
- Implement **AI-based path planning** for improved navigation.
- Add **real-time telemetry feedback** over Wi-Fi.
- Optimize **RC controller mappings** for better maneuverability.

---

## Author
**Aditya Chatterjee** 🚀
