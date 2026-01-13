
---
title: SEC-IoT - Secure Industrial IoT Monitoring & Analytics Platform
description: ESP32 + Flask + XAMPP IoT Dashboard for Industrial Monitoring
---

# 🔐 SEC-IoT  
**Secure Industrial IoT Monitoring & Analytics Platform**

---

### 🗂️ SEC-IoT Project Index

* [🔐 SEC-IoT Overview](#🔐-sec-iot)  
* [🏗️ System Architecture](#🏗️-system-architecture)
* [🧩 Hardware Connection Diagram](#🧩-hardware-connection-diagram-and-software-working)
* [🔌 Hardware Pin Mapping](#🔌-hardware-components-used-with-esp32-sensor-pin-mapping-sec-iot)
* [🔧 Arduino Firmware Setup](#🔧-arduino-ide-requirements--sec-iot-firmware)
* [🗂️ Project Folder Structure](#🗂️-project-folder-structure)
* [🗄️ Database Schema Details](#🗄️-database-setup-xampp)
* [⚙️ Software Requirements](#⚙️-software-requirements)
* [🚀 Methodology & Workflow](#🚀-methodology-workflow)
* [📡 Network Requirements](#📡-network-requirement-important)
* [▶️ Running the Project](#▶️-running-the-project-localhost)
* [🧪 API Endpoint](#🧪-api-endpoint-used-by-esp32)
* [🚀 Automation & Quick Start](#🚀-automation--quick-start)
* [🔮 Future Work](#🔮-future-work)

---

# 🔐 SEC-IoT  
**Secure Industrial IoT Monitoring & Analytics Platform**

SEC-IoT is an end-to-end **Industrial IoT monitoring system** that integrates **ESP32-based sensor nodes**, a **Flask web dashboard**, **XAMPP (MySQL) backend**, and is designed to be **ML-ready** for future prediction, security, and explainable AI (XAI) extensions.

This project is developed for **academic, industrial automation, and research purposes**. [web:11]

---

## 📌 Project Features

- 📡 **Real-time sensor data acquisition** using ESP32  
- 🌐 **Localhost Flask-based IoT Dashboard**  
- 🗄️ **MySQL (XAMPP) database storage**  
- 📊 **Interactive charts & tables** (Chart.js)  
- 🌙 **Dark / ☀️ Light mode UI**  
- 👤 **User authentication & profile management**  
- 🔐 **Secure IoT-ready architecture**  
- 🧠 **Future-ready for ML and Security research**  

---

## 🏗️ System Architecture

```
[ Sensors ] → [ ESP32 ] → [ WiFi (2.4 GHz) ] → [ Flask Server ]
                                     ↓
                              [ XAMPP MySQL ]
                                     ↓
                           [ SEC-IoT Web Dashboard ]
```

> 📷 **System architecture diagram:** [IoT_Project_Diagram.png](IoT_Project_Diagram.png)

---

## 🧩 Hardware Connection Diagram and Software Working

Below is the complete **hardware connection diagram** for the SEC-IoT system.

![SEC-IoT Hardware Connection Diagram](IoT_Project_Diagram.png)

> 📌 **Important Notes:**  
> - Ensure all sensors and ESP32 share a **common GND**  
> - Use a **voltage divider** for HC-SR04 ECHO pin  
> - Power ESP32 via **USB or VIN (5V)**  
> - Use **3.3V only** for GPIO-safe sensors  

---

## 🔌 Hardware Components Used with ESP32 Sensor Pin Mapping (SEC-IoT)

| Sensor / Component | Sensor Pin | ESP32 GPIO | VCC | GND | Notes |
|-------------------|-----------|------------|-----|-----|------|
| **Ultrasonic Sensor (HC-SR04)** | TRIG | GPIO 5 | 3.3V | GND | Trigger pin |
| | ECHO | GPIO 18 | 3.3V | GND | ⚠️ Use voltage divider |
| | VCC | — | 3.3V | — | Avoid 5V on ESP32 |
| | GND | — | — | GND | Common ground |
| **Temperature & Humidity Sensor (DHT11 / DHT22)** | DATA | GPIO 4 | 3.3V | GND | Single-wire data |
| | VCC | — | 3.3V | — | — |
| | GND | — | — | GND | — |
| **Gas Sensor (MQ-135)** | AO (Analog Out) | GPIO 34 (ADC) | 3.3V | GND | ADC-only pin |
| | VCC | — | 3.3V | — | Stable ADC |
| | GND | — | — | GND | — |
| **Current Sensor (ACS712)** | OUT | GPIO 15 (ADC) | 5V (VIN) | GND | Output ≤ 3.3V |
| | VCC | — | VIN (5V) | — | Powered via VIN |
| | GND | — | — | GND | — |
| **ESP32 Dev Board** | — | — | USB / VIN (5V) | GND | Main controller |

⚠️ **Critical:** ESP32 is **3.3V logic** — use voltage dividers where needed. [web:11]

---

# 🔧 Arduino IDE Requirements – SEC-IoT Firmware

This document lists all **required Arduino IDE packages, libraries, and setup steps** needed to compile and upload the **SEC-IoT ESP32 firmware**.

## 🧠 Supported Hardware
- **ESP32 Dev Module**
- Arduino IDE **v1.8.x or v2.x**
- WiFi Network: **2.4 GHz only**

## 1️⃣ Install Arduino IDE
[Download Arduino IDE](https://www.arduino.cc/en/software)

## 2️⃣ Add ESP32 Board Support (MANDATORY)

**Board Manager URL:**  
```
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

**Steps:**
1. **Tools → Board → Boards Manager**
2. Search: `ESP32`
3. Install **"esp32 by Espressif Systems"**

## 3️⃣ Required Arduino Libraries

Install via **Sketch → Include Library → Manage Libraries**:

| Library Name | Author | Used For |
|-------------|--------|---------|
| DHT sensor library | Adafruit | DHT22 Temperature & Humidity |
| Adafruit Unified Sensor | Adafruit | DHT dependency |
| ArduinoJson | Benoit Blanchon | JSON payload generation |
| WiFi | ESP32 Core | WiFi connectivity |
| HTTPClient | ESP32 Core | HTTP POST to Flask API |

**ArduinoJson version:** v6.x recommended.

## 4️⃣ Board & Port Configuration

- **Board:** ESP32 Dev Module  
- **Upload Speed:** 115200  
- **CPU Frequency:** 240MHz  
- **Flash Frequency:** 80MHz  
- **Flash Mode:** QIO  

## 5️⃣ Common Errors & Fixes

| Error | Fix |
|-------|-----|
| HTTP Response -1 | Flask server not reachable / firewall blocking |
| WiFi not connecting | 5GHz network used (ESP32 supports only 2.4GHz) |
| DHT returns NaN | Wrong pin connection or incorrect power |
| ESP32 not detected | Install USB-to-UART driver |

---

## 🗂️ Project Folder Structure

```
SEC-IoT/
│
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── run_n_go.bat          # One-click Windows setup
├── README.md             # This file
│
├── static/
│   ├── css/style.css     # Dashboard styling
│   ├── js/charts.js      # Chart.js integration
│   └── uploads/          # User profile pictures
│
├── templates/
│   ├── base.html         # Base template
│   ├── login.html        # Login page
│   ├── dashboard.html    # Main dashboard
│   ├── profile.html      # User profile
│   └── admin.html        # Admin panel
│
└── Firmware/
    └── IoT_Project_Firmware.ino  # ESP32 source code
```

---

## ⚙️ Software Requirements

- **Python 3.9+**
- **Flask** + **Flask-Login**
- **MySQL (XAMPP)**
- **Arduino IDE**
- **Browser** (Chrome / Firefox)

**requirements.txt:**
```
Flask==2.3.3
Flask-Login==0.6.3
mysql-connector-python==8.2.0
Werkzeug==2.3.7
```

---

## 🗄️ Database Setup (XAMPP)

### 1️⃣ Create Database

```sql
CREATE DATABASE iot_dashboard;
USE iot_dashboard;
```

### 2️⃣ Users Table

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    profile_pic VARCHAR(255) DEFAULT 'default.png'
);
```

### 3️⃣ Sensor Data Table

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

## 🚀 Methodology (Workflow)

1. **Sensors** → ESP32 (GPIO pins)
2. **ESP32** programmed using Arduino IDE
3. **ESP32** sends JSON data over HTTP
4. **Flask** (`app.py`) receives & stores in MySQL
5. **SEC-IoT Dashboard** visualizes real-time data

---

## 📡 Network Requirement (IMPORTANT)

⚠️ **ESP32 and Flask Server MUST be on the SAME network**

```
✔ 2.4 GHz WiFi ONLY (ESP32 does NOT support 5 GHz)
✔ Same SSID & WiFi password
✔ Same subnet (192.168.x.x)
```

**Firmware config example:**
```cpp
WiFi.begin("YOUR_WIFI_NAME", "YOUR_WIFI_PASSWORD");
const char* serverURL = "http://192.168.1.100:5000/api/add_data";
```

---

## ▶️ Running the Project (Localhost)

### 1️⃣ Start XAMPP
```
Apache ✅ | MySQL ✅
```

### 2️⃣ Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run Flask Server
```bash
python app.py
```
**Access:** `http://localhost:5000`

### 4️⃣ Upload ESP32 Firmware
- Open Arduino IDE
- Load `Firmware/IoT_Project_Firmware.ino`
- Select ESP32 board & COM port
- Upload

---

## 🧪 API Endpoint Used by ESP32

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

## 🚀 Automation & Quick Start

### ⚡ **One-Click Windows Setup** (`run_n_go.bat`)

1. **Start XAMPP** (Apache + MySQL)
2. Double-click **`run_n_go.bat`** in project root
3. Browser opens automatically: `http://localhost:5000`

**What `run_n_go.bat` does:**
```batch
@echo off
pip install -r requirements.txt
python app.py
pause
```

### 🏃 **Manual CMD Setup**
```cmd
cd SEC-IoT
pip install -r requirements.txt
python app.py
```

---

## 🔮 Future Work

- **🧠 ML Predictions** (temperature, gas levels)
- **🔍 XAI Interpretability** (SHAP/LIME)
- **🛡️ IoT Intrusion Detection**
- **☁️ Cloud Deployment** (AWS IoT Core)
- **📱 Mobile App** (Flutter/React Native)

---

## 📄 License

**Academic & Educational Use Only**  
Fork, modify, and experiment responsibly.

---

## 👤 Author & Credits

**Project:** SEC-IoT  
**Developed By:** SEC-IoT Team  

**Tech Stack:**
- **Firmware:** Arduino (ESP32) [web:11]
- **Backend:** Flask + MySQL  
- **Frontend:** HTML/CSS/Chart.js  

> *"Secure, Analyze, Predict — The Future of Industrial IoT"* 🚀

---

⭐ **Star the repo** if this helps! 📈

---
