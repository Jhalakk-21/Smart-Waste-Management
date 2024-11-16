# Smart-Waste-Management

## Directory structure:
  The folder models contains the code of 4 models we trained and have presented.
  The folder lite-models contains the tensorflow lite versions of first, second and fourth model above. They can be used to run and check the working. Their paths needed to be added in the main\_code.py
  The file main_code.py includes the code for the image capturing, classification using the model, and running the motor.
  The Arduino code is to run the ultrasonic distance sensors.
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
  - fswebcam
  - numpy
  - opencv-python
  - tflite-runtime
  - gpiozero
  - paho.mqtt.client
  - json
  - tkinter
  - matplotlib
- Arduino Libraries:
  - NewPing
  - ESP8266WiFi.h
  - PubSubClient.h

### *Python Libraries Installation (for Raspberry Pi)*
```bash
pip install RPi.GPIO
