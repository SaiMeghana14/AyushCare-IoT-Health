# AyushCare – Rural Health Monitoring with IoT

![AyushCare Banner][https://github.com/yourusername/ayushcare-iot/blob/main/AyushCare_Banner.png?raw=true]

## 💡 Project Overview

**AyushCare** is a smart IoT-based health monitoring system designed to support **rural communities** by enabling real-time tracking of vital signs like **heart rate, SpO₂, body temperature**, and **blood pressure**. This system sends patient data to the cloud, allowing **remote doctors** and **health workers** to monitor health conditions and provide timely alerts and intervention.

---

## 🎯 Key Features

- 📡 Real-time monitoring of vital parameters (HR, SpO₂, Temp, BP)
- ☁️ Cloud integration using **Blynk IoT** / **Firebase**
- 📱 Doctor dashboard for patient history and alerts
- 🔔 Instant mobile notifications for abnormal values
- 🧾 Patient health record storage
- 🌍 Designed for **low-resource, rural environments**

---

## 🧩 Components Used

| Component          | Description                        |
|-------------------|------------------------------------|
| ESP32 / NodeMCU    | Wi-Fi-enabled microcontroller      |
| MAX30100 Sensor    | Measures Heart Rate and SpO₂       |
| LM35 / DS18B20     | Measures Body Temperature          |
| OLED/LCD Display   | Displays local sensor data         |
| Blynk / Firebase   | Cloud sync and dashboard           |
| Arduino IDE        | Code development environment       |

---

## 🛠️ How It Works

1. Sensors collect patient vitals.
2. ESP32/NodeMCU reads sensor data and sends it to Blynk/Firebase.
3. Data is displayed on:
   - Local OLED/LCD for health workers
   - Blynk mobile app for doctors/relatives
4. Alerts are triggered if vitals cross safety thresholds.
5. All readings are stored for future medical reference.

---

## 🖥️ Screenshots

> 🔧 [Add screenshots of app dashboard and circuit here]

---

## 🚀 Future Enhancements

- AI-based anomaly detection
- SMS gateway support for remote areas
- Offline-first architecture with local caching
- Voice or video teleconsultation integration

---

## 📁 Repository Structure

AyushCare/
├── Arduino_Code/
│ └── ayushcare_monitor.ino
├── Mobile_Dashboard/
│ └── blynk_setup_guide.pdf
├── Circuit_Diagram/
│ └── ayushcare_circuit.fzz
├── UI_Mockups/
│ └── doctor_dashboard_mockup.png
├── Docs/
│ └── project_report.pdf
└── README.md

---

## 📦 Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/yourusername/ayushcare-iot.git
   cd ayushcare-iot
2. Open ayushcare_monitor.ino in Arduino IDE

- Install libraries: Blynk, Adafruit_Sensor, MAX30100lib, etc.

3.Setup your Blynk template or Firebase project

- Follow instructions in Mobile_Dashboard/blynk_setup_guide.pdf

4.Upload code to ESP32/NodeMCU

- Power up and test sensors

- Monitor on Blynk or Firebase dashboard

👤 Author
K.N.V Sai Meghana 
B.Tech ECE | IoT & Embedded Systems
🔗 GitHub: saimeghana
🔗 LinkedIn: Naga Venkata Sai Meghana Kovvada

🔗 Project Link
👉 View project here ([View the dashboard](https://ayushcare-iot-health-pmksxk7ces2cg9rt54anm2.streamlit.app/))]

**Note**
##Enter the following credentials- 
     [Username - doctor and Password - 1234]
     
📃 License
This project is licensed under the MIT License.
