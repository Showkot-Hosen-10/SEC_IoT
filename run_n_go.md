---

# 🚀 Quick Start Guide: SEC-IoT (Run-n-Go)

Follow these steps to get the system running locally from scratch.

### 1. 🔌 Hardware Setup (ESP32 Mapping)

Connect your sensors to the ESP32 according to this table. Ensure a **Common GND**.

| Component | Sensor Pin | ESP32 GPIO | Voltage | Note |
| --- | --- | --- | --- | --- |
| **Ultrasonic** | TRIG / ECHO | GPIO 5 / 18 | 3.3V | Use divider for ECHO |
| **DHT11/22** | DATA | GPIO 4 | 3.3V | 10k Resistor if needed |
| **Gas (MQ)** | AO (Analog) | GPIO 34 | 3.3V | Warm up for 20s |
| **Current** | OUT (Analog) | GPIO 15 | 5V (VIN) | ACS712 Module |

### 2. 📡 Firmware Upload

1. Open `Firmware/IoT_Project_Firmware.ino` in Arduino IDE.
2. Update `SSID`, `PASSWORD`, and `serverURL` (Use your PC's Local IP).
3. Select **Board: ESP32 Dev Module** and click **Upload**.
4. Open **Serial Monitor (115200)** to verify "Data Sent Successfully".

### 3. 💻 Database & Flask Setup (CMD)

Open **XAMPP Control Panel**, start **Apache** and **MySQL**. Click **Shell** in XAMPP or open your terminal and run:

```cmd
:: 1. Clone and Enter Project
git clone https://github.com/Showkot-Hosen-10/SEC_IoT.git && cd SEC_IoT

:: 2. Create Database (Run this in XAMPP MySQL Shell or phpMyAdmin)
mysql -u root -e "CREATE DATABASE iot_dashboard;"

:: 3. Setup Python Environment & Dependencies
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt

:: 4. Run the Platform
python app.py

```

### 4. 🌐 Access the Dashboard

Once the flask server starts, open your browser and go to:
`http://localhost:5000`

---

### 🛠 Troubleshooting

* **Database Connection:** Ensure XAMPP MySQL is running on port 3306.
* **ESP32 Connection:** Both PC and ESP32 **must** be on the same 2.4GHz WiFi.
* **Firewall:** If data isn't reaching Flask, allow Port 5000 in Windows Firewall.

---

**Would you like me to generate the SQL script file separately so you can import it with a single command?**
