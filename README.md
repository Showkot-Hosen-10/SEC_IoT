# SEC-IoT  
**Secure Industrial IoT Monitoring & Analytics Platform**

---

## 📋 Project Index

* [SEC-IoT Overview](#sec-iot-overview)
* [System Architecture](#system-architecture)
* * [Project Folder Structure](#project-folder-structure)
* [Hardware Connection](#hardware-connection)
* [Hardware Pin Mapping](#hardware-pin-mapping)
* [Arduino Firmware Setup](#arduino-firmware-setup)
* [Database Schema](#database-schema)
* [Software Requirements](#software-requirements)
* * [Methodology](#methodology)
* [Network Requirements](#network-requirements)
* [Running the Project](#running-the-project)
* [API Endpoint](#api-endpoint)
* [Quick Start](#automation-quick-start)
* [Future Work](#future-work)

---

## SEC-IoT Overview

SEC-IoT is an end-to-end **Industrial IoT monitoring system** that integrates **ESP32-based sensor nodes**, a **Flask web dashboard**, **XAMPP (MySQL) backend**, and is designed to be **ML-ready** for future prediction, security, and explainable AI (XAI) extensions.

**Target Use Cases:**
- Academic research and thesis projects
- Industrial automation monitoring
- Security research and CTF challenges

### Project Features
- 📡 Real-time sensor data acquisition using ESP32
- 🌐 Localhost Flask-based IoT Dashboard
- 🗄️ MySQL (XAMPP) database storage
- 📊 Interactive charts & tables (Chart.js)
- 🌙 Dark/Light mode UI
- 👤 User authentication & profile management
- 🔐 Secure IoT-ready architecture
- 🧠 Future-ready for ML and Security research

---

## System Architecture

```
[ Sensors ] → [ ESP32 ] → [ WiFi (2.4 GHz) ] → [ Flask Server ]
                                     ↓
                              [ XAMPP MySQL ]
                                     ↓
                           [ SEC-IoT Web Dashboard ]
```

**System Flow:**
1. Sensors → ESP32 GPIO pins
2. ESP32 → WiFi → HTTP POST to Flask API
3. Flask → MySQL storage
4. Dashboard → Real-time visualization

---

## Hardware Connection

![SEC-IoT Hardware Diagram](IoT_Project_Diagram.png)

### Connection Notes
- **Common GND** for all sensors
- **Voltage divider** for HC-SR04 ECHO pin
- **ESP32 Power:** USB or VIN (5V)
- **GPIO-safe sensors:** 3.3V only

---

## Hardware Pin Mapping

| Sensor | Pin | ESP32 GPIO | VCC | GND | Notes |
|--------|-----|------------|-----|-----|-------|
| **HC-SR04 Ultrasonic** | TRIG | GPIO 5 | 3.3V | GND | Trigger |
| | ECHO | GPIO 18 | 3.3V | GND | Voltage divider |
| **DHT11/DHT22** | DATA | GPIO 4 | 3.3V | GND | Single wire |
| **MQ-135 Gas** | AO | GPIO 34 | 3.3V | GND | ADC only |
| **ACS712 Current** | OUT | GPIO 15 | 5V(VIN) | GND | Output ≤ 3.3V |

⚠️ **ESP32 = 3.3V logic** - Use voltage dividers where needed.

---

## Arduino Firmware Setup

### Supported Hardware
```
ESP32 Dev Module | Arduino IDE v1.8.x/v2.x | 2.4GHz WiFi
```

### 1. Install Arduino IDE
[Download](https://www.arduino.cc/en/software)

### 2. ESP32 Board Support
**Board Manager URL:**
```
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

**Install:** `esp32 by Espressif Systems`

### 3. Required Libraries
| Library | Author | Purpose |
|---------|--------|---------|
| DHT sensor library | Adafruit | Temperature/Humidity |
| Adafruit Unified Sensor | Adafruit | DHT dependency |
| ArduinoJson | Benoit Blanchon | JSON payloads |
| WiFi | ESP32 Core | Connectivity |
| HTTPClient | ESP32 Core | API calls |

### 4. Board Settings
```
Board: ESP32 Dev Module
Upload Speed: 115200
CPU: 240MHz
Flash: 80MHz (QIO)
```

---

## Project Folder Structure

```
SEC-IoT/
├── app.py                 # Flask backend
├── requirements.txt       # Python deps
├── run_n_go.bat          # Windows setup
├── README.md            # This file
│
├── static/
│   ├── css/style.css
│   ├── js/charts.js
│   └── uploads/
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── profile.html
│   └── admin.html
│
└── Firmware/
    └── IoT_Project_Firmware.ino
```

---

## Database Schema

### 1. Create Database
```sql
CREATE DATABASE iot_dashboard;
USE iot_dashboard;
```

### 2. Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    profile_pic VARCHAR(255) DEFAULT 'default.png'
);
```

### 3. Sensor Data
```sql
CREATE TABLE sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ultrasonic FLOAT,
    temperature FLOAT,
    humidity FLOAT,
    mq135 FLOAT,
    current_mA FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Software Requirements

```
Python 3.9+ | Flask | MySQL(XAMPP) | Arduino IDE | Chrome/Firefox
```

**requirements.txt:**
```
Flask==2.3.3
Flask-Login==0.6.3
mysql-connector-python==8.2.0
Werkzeug==2.3.7
```

---

## Methodology

```
Sensors → ESP32 → WiFi → Flask API → MySQL → Dashboard
```

1. **ESP32** reads sensors every 5 seconds
2. **JSON payload** sent via HTTP POST
3. **Flask** stores data in MySQL
4. **Dashboard** shows live charts

---

## Network Requirements

⚠️ **Critical: ESP32 + Flask on SAME network**

```
2.4GHz WiFi ONLY
Same SSID/password
Same subnet (192.168.x.x)
Firewall: Allow port 5000
```

**Firmware config:**
```cpp
WiFi.begin("WIFI_SSID", "WIFI_PASS");
const char* serverURL = "http://192.168.1.100:5000/api/add_data";
```

---

## Running the Project

### 1. Start XAMPP
```
Apache ✅ MySQL ✅
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Flask
```bash
python app.py
```
**URL:** `http://localhost:5000`

### 4. Upload Firmware
```
Arduino IDE → Firmware/IoT_Project_Firmware.ino → Upload
```

---

## API Endpoint

```
POST http://<PC_IP>:5000/api/add_data
```

**JSON Payload:**
```json
{
  "ultrasonic": 50.2,
  "temperature": 28.5,
  "humidity": 65.0,
  "mq135": 320.0,
  "current_mA": 120.0
}
```

---

## Automation & Quick Start

### One-Click Setup (Windows)
```
1. Start XAMPP (Apache+MySQL)
2. Double-click run_n_go.bat
3. http://localhost:5000 opens automatically
```

**run_n_go.bat:**
```batch
@echo off
echo Starting SEC-IoT...
pip install -r requirements.txt
python app.py
pause
```

### Manual Setup
```cmd
cd SEC-IoT
pip install -r requirements.txt
python app.py
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| HTTP -1 | Flask not running / firewall |
| WiFi fail | Use 2.4GHz network |
| DHT NaN | Check wiring / power |
| ESP32 not found | Install USB drivers |

---

## Future Work

- 🧠 **ML Predictions** (LSTM, Prophet)
- 🔍 **XAI** (SHAP/LIME explanations)
- 🛡️ **IoT IDS** (anomaly detection)
- ☁️ **Cloud** (AWS IoT Core)
- 📱 **Mobile App** (Flutter)

---

## License

**Academic & Educational Use Only**

---

## Authors

**SEC-IoT Team**  
**Tech:** ESP32 | Flask | MySQL | Chart.js

> *"Secure. Analyze. Predict. — Industrial IoT"* 🚀

---
⭐ **Star if helpful!**
```
