# 🌿 AyushCare – AI-Powered Rural Health Monitoring System

![AyushCare Banner](https://raw.githubusercontent.com/SaiMeghana14/AyushCare-IoT-Health/refs/heads/main/AyushCare_banner.png)

---

# 🏥 Project Overview

**AyushCare** is an advanced **AI-powered IoT healthcare monitoring platform** designed to improve healthcare accessibility in **rural and remote communities**.

The system continuously monitors critical patient vitals such as:

- ❤️ Heart Rate
- 🫁 SpO₂ (Oxygen Saturation)
- 🌡 Body Temperature
- 🩸 Blood Pressure
- 🌬 Respiratory Rate

using **IoT sensors**, **AWS cloud services**, and an intelligent real-time analytics dashboard.

AyushCare enables:

✅ Real-time patient monitoring  
✅ Emergency alert detection  
✅ AI-powered health insights  
✅ Cloud-based patient history storage  
✅ Multi-patient hospital dashboard  
✅ Remote healthcare assistance for rural areas  

---

# 🚀 Live Demo

🌐 **Streamlit Dashboard**  
👉 https://ayushcare-iot-health-pmksxk7ces2cg9rt54anm2.streamlit.app/

---

# ✨ Key Features

## 📡 Real-Time IoT Monitoring
- Continuous live patient vitals tracking
- Simulated ESP32 device feed
- Live ECG monitoring visualization
- Real-time dashboard refresh

---

## ☁ AWS Cloud Integration

AyushCare uses AWS services for scalable cloud healthcare monitoring.

### Integrated AWS Services:
- 🗄 **Amazon DynamoDB** → Patient vitals storage
- 📨 **Amazon SNS** → Emergency SMS alerts
- ☁ AWS Cloud Connectivity Status
- 🔒 Secure health data transmission

---

## 🧠 AI Health Insights
- AI-based patient risk analysis
- Smart health score generation
- Emergency risk prediction
- Automated health recommendations

### Example Predictions:
- No immediate health risk detected
- Oxygen trend stable
- Continuous monitoring recommended
- Critical oxygen fluctuation detected

---

## 🚨 Emergency Alert System
Automatically triggers emergency mode when:
- SpO₂ drops below safe levels
- Temperature becomes critical
- Heart rate abnormalities are detected

### Emergency Features:
- Emergency alert banner
- AWS SNS notification support
- Critical risk detection
- Real-time monitoring escalation

---

## 🏥 Multi-Patient Monitoring Dashboard
Hospital-style centralized monitoring system.

### Includes:
- Multiple patient overview
- Risk categorization
- Real-time patient status
- Health analytics dashboard

---

## 📈 Advanced Healthcare Analytics
- Live vitals charts
- Historical patient trends
- ECG simulation
- Rural healthcare coverage map
- Interactive Plotly visualizations

---

# 🧩 Technologies Used

| Category | Technologies |
|---|---|
| Frontend | Streamlit, HTML, CSS |
| Cloud | AWS DynamoDB, AWS SNS |
| Data Visualization | Plotly, Pandas |
| IoT | ESP32, MAX30102 |
| Backend | Python |
| AI Logic | Custom Risk Analysis Engine |
| Database | DynamoDB + JSON History Storage |

---

# ⚙ System Architecture

```text
IoT Sensors → ESP32 → AWS Cloud → Streamlit Dashboard → AI Analysis → Emergency Alerts
```

---

# 🛠 Components Used

| Component | Description |
|---|---|
| ESP32 / NodeMCU | Wi-Fi-enabled IoT controller |
| MAX30102 Sensor | Heart Rate + SpO₂ Sensor |
| Temperature Sensor | Body Temperature Monitoring |
| OLED/LCD | Local Display |
| AWS DynamoDB | Cloud Database |
| AWS SNS | Emergency Alerts |
| Streamlit | Real-Time Dashboard |
| Plotly | Interactive Graphs |

---

# 🖥 Dashboard Features

## 🌿 Smart Rural Healthcare Interface
Modern hospital-style UI designed for healthcare accessibility.

### Includes:
- Live status cards
- Health score gauge
- ECG monitor
- Device feed simulation
- AI predictions
- Emergency timeline
- Rural healthcare coverage map
- Multi-patient monitoring

---

# 📊 Sample Health Metrics

| Metric | Value |
|---|---|
| Heart Rate | 74 BPM |
| SpO₂ | 98% |
| Temperature | 36.8°C |
| Health Score | 100/100 |
| Risk Level | Low |

---

# 🧠 AI Risk Levels

| Score Range | Risk Level |
|---|---|
| 85 – 100 | 🟢 Low |
| 60 – 84 | 🟡 Moderate |
| Below 60 | 🔴 Critical |

---

# 📁 Project Structure

```text
AyushCare/
│
├── app.py
├── users.json
├── sample_vitals.json
├── history.json
├── requirements.txt
│
├── components/
│   ├── sidebar.py
│   ├── status_card.py
│   ├── ai_predictions.py
│   ├── charts.py
│   ├── emergency.py
│   ├── metrics.py
│   ├── doctor_notes.py
│   ├── patient_monitor.py
│   ├── device_feed.py
│   └── health_map.py
│
├── services/
│   ├── aws_service.py
│   ├── alerts.py
│   ├── history_service.py
│   ├── data_loader.py
│   └── auth_service.py
│
├── views/
│   ├── login.py
│   ├── register.py
│   └── dashboard.py
```

---

# 📦 Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/SaiMeghana14/AyushCare-IoT-Health.git

cd AyushCare-IoT-Health
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Configure AWS Secrets

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
AWS_ACCESS_KEY_ID = "YOUR_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "YOUR_SECRET_KEY"
AWS_REGION = "ap-south-1"
```

---

## 4️⃣ Run Streamlit App

```bash
streamlit run app.py
```

---

# ☁ AWS Services Used

## 🗄 Amazon DynamoDB
Stores:
- Patient vitals
- Historical records
- Monitoring data

---

## 📨 Amazon SNS
Used for:
- Emergency SMS alerts
- Critical health notifications

---

# 🌍 Rural Healthcare Impact

AyushCare aims to:
- Improve healthcare accessibility
- Support remote patient monitoring
- Enable faster emergency response
- Assist doctors in rural areas
- Reduce healthcare infrastructure gaps

---

# 🔮 Future Enhancements

- 🤖 Real AI/ML anomaly detection
- 📹 Telemedicine integration
- 📱 Mobile healthcare app
- 🌐 AWS IoT Core integration
- 📡 Real ESP32 live streaming
- 🧬 Predictive health analytics
- 🗣 Voice-based emergency alerts

---

# 👤 Author

## **K.N.V Sai Meghana**
B.Tech – Electronics & Communication Engineering (ECE)

### 🔗 GitHub
https://github.com/SaiMeghana14

### 🔗 LinkedIn
https://www.linkedin.com/in/naga-venkata-sai-meghana-kovvada131b51259

---

# 📄 License

This project is licensed under the MIT License.

---

# ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!
