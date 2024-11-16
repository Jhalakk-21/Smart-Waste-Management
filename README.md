# Smart-Waste-Management
# *Servo Motor, Stepper Motor, and Ultrasonic Distance Sensors Integration*

## *Project Overview*

This project integrates a *Servo Motor, a **Stepper Motor, and two **Ultrasonic Distance Sensors* using a *Raspberry Pi* and *Arduino Uno*. The system is designed to control motors based on distance measurements from the sensors, enabling various automation tasks such as object detection and motor movements based on the detected distances.

## *Table of Contents*
- [Project Overview](#project-overview)
- [Components Used](#components-used)
- [Wiring and Connections](#wiring-and-connections)
- [Software Requirements](#software-requirements)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [License](#license)

## *Components Used*
- Raspberry Pi 3/4 B+
- Arduino Uno
- Servo Motor
- Stepper Motor with Driver Module (ULN2003 or L298N)
- 2x Ultrasonic Distance Sensors (HC-SR04)
- Jumper Wires
- Breadboard
- Power Supply

## *Wiring and Connections*

### *1. Servo Motor (Connected to Raspberry Pi)*
| Servo Motor Pin | Raspberry Pi Pin |
|-----------------|------------------|
| GND             | GND              |
| 5V              | 5V               |
| Signal (Input)  | GPIO 21          |

### *2. Stepper Motor (Connected to Raspberry Pi via Driver Module)*
| Driver Module Pin | Raspberry Pi Pin |
|-------------------|------------------|
| VCC (12V)         | 5V               |
| GND               | GND              |
| IN1               | GPIO 14          |
| IN2               | GPIO 15          |
| IN3               | GPIO 18          |
| IN4               | GPIO 23          |

### *3. Ultrasonic Distance Sensor 1 (Connected to Arduino Uno)*
| Ultrasonic Sensor Pin | Arduino Uno Pin |
|-----------------------|-----------------|
| VCC                   | 5V              |
| GND                   | GND             |
| Trig                  | 4               |
| Echo                  | 2               |

### *4. Ultrasonic Distance Sensor 2 (Connected to Arduino Uno)*
| Ultrasonic Sensor Pin | Arduino Uno Pin |
|-----------------------|-----------------|
| VCC                   | 5V              |
| GND                   | GND             |
| Trig                  | 7               |
| Echo                  | 8               |

## *Software Requirements*
- Python 3.x
- Arduino IDE
- Python Libraries:
  - RPi.GPIO
  - time
- Arduino Libraries:
  - NewPing

### *Python Libraries Installation (for Raspberry Pi)*
```bash
pip install RPi.GPIO
