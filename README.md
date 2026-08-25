# 📁 Smart File Analyzer (Enterprise Edition)

[![Streamlit App](https://img.shields.io/badge/Streamlit-1.42+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Machine Learning](https://img.shields.io/badge/Scikit--Learn-ML_Clustering-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Database](https://img.shields.io/badge/SQLite-Auth_%26_Audit_Logs-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

An enterprise-grade, interactive **Streamlit Web Application** designed for multi-file metadata processing, cryptographic SHA-256 duplicate detection, AI-powered storage diagnostics, Machine Learning anomaly detection, real-time hardware telemetry, and SQL user audit logging.

---

## 🌟 Key Highlights & Features

### 🔐 1. Mandatory User Authentication & Security
- **Secure Access Control**: Mandatory login/signup gatekeeper before application content access.
- **Cryptographic Hashing**: User passwords hashed with **SHA-256 + Salt**.
- **Persistent SQL User Sessions**: User accounts and audit logs stored in relational **SQLite3** database (`database/app_data.db`).

### 🎨 2. Top-Right Appearance Theme Switcher
- **Dynamic Theme Modes**: Easily switch between **Dark Glassmorphism**, **Corporate Light**, and **System Auto-Detect** modes via the top-right header selector.
- **Custom CSS Engine**: Sleek cards, responsive metrics, glowing accents, and smooth micro-animations.

### 📂 3. Multi-File Analyzer & Hashing Engine
- **Universal Format Support**: Upload `.csv`, `.xlsx`, `.pdf`, `.txt`, `.docx`, images (`.png`, `.jpg`), `.zip`, `.json`, `.py`, and more.
- **Metadata Extraction**: Calculates file extension, human-readable size (Bytes, KB, MB, GB), and general category (Documents, Images, Videos, Audio, Archives, Data, Code, Other).
- **🔁 SHA-256 Duplicate Detection**: Cryptographically detects identical file content and calculates wasted storage space.
- **📦 Top 10 Storage Hogs**: Ranks top largest uploaded files.
- **📊 Interactive Visualizations**: Plotly distribution bar charts, storage per file category, and horizontal top file size charts.
- **🔍 Granular Filtering**: Filter files by category, minimum size, and maximum size.

### 🤖 4. AI Storage Insights & Health Advisor
- **Storage Health Index**: Calculates a 0–100 health rating based on duplicate waste and file distribution.
- **Smart AI Recommendations**: Generates automated file cleanup advisories and security risk alerts.
- **Flexible API Integration**: Enter optional **OpenAI / Gemini API Keys**, or utilize the built-in AI NLP heuristics engine.

### 🧠 5. Complex Machine Learning Engine
- **🛡️ IsolationForest Anomaly Detection**: Unsupervised ML model that flags abnormal file sizes and extension outliers with interactive Plotly scatter plots.
- **📊 K-Means Storage Clustering**: Machine Learning clustering algorithm that automatically groups uploaded files into $k$ smart storage tiers.

### 💻 6. System Information Telemetry (Mandatory Page)
- **Live Hardware Monitoring**: Reads host CPU cores, current CPU usage %, RAM total/used/free, disk partition space, and OS environment specs using `psutil` and `platform`.
- **Live Progress Gauges**: Real-time meters for CPU, RAM, and Disk space utilization.
- **Refresh Telemetry**: Interactive refresh button to re-fetch system stats.

### 📜 7. SQL Database Audit Logs
- Automatically logs all analyzed file records for authenticated users into SQLite database table (`analysis_logs`).

---

## 🏗️ Architecture & Project Structure

```
Smart-File-Analyzer/
│
├── app.py                     # Main Streamlit Application & Multi-Page Router
├── requirements.txt           # Python dependencies (streamlit, pandas, plotly, psutil, scikit-learn, numpy)
├── README.md                  # Comprehensive Documentation & Setup Guide
├── .gitignore                 # Git ignore rules
├── Procfile                   # Heroku / Render Cloud deployment file
│
├── .streamlit/
│   └── config.toml            # Streamlit theme & cloud configuration
│
├── database/
│   └── app_data.db            # SQLite SQL database (auto-generated)
│
├── utils/
│   ├── __init__.py            # Package initialization
│   ├── theme_css.py           # CSS design system & Theme switcher (Light/Dark/System)
│   ├── auth_db.py             # User Auth, Password Hashing, SQL database handler
│   ├── ai_engine.py           # AI Insights, Storage Health Index, and API handler
│   ├── ml_engine.py           # Scikit-Learn IsolationForest Anomaly Detection & KMeans Clustering
│   ├── file_analyzer.py       # Metadata extraction, SHA-256 duplicate detection, category classifier
│   └── system_info.py         # Hardware specs, CPU, RAM, Disk, OS telemetry
│
└── assets/
    └── .gitkeep               # Asset folder tracker
```

---

## ⚡ Quick Start Guide

### Prerequisites
- **Python 3.10+**
- **Git**

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/<YOUR_USERNAME>/Smart-File-Analyzer.git
   cd Smart-File-Analyzer
   ```

2. **Create & Activate Virtual Environment**
   - **Windows (PowerShell / CMD):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Application**
   ```bash
   streamlit run app.py
   ```

5. Access the app at `http://localhost:8501`.

---

## 🔄 Data Processing Pipeline

```
Uploaded Files
     ↓
Extract Metadata & SHA-256 Hashes
     ↓
Classify Extension Categories & Sizes
     ↓
Detect SHA-256 Duplicates & Top Hogs
     ↓
Run ML IsolationForest & KMeans Clustering
     ↓
Generate AI Storage Health Index & Advice
     ↓
Store SQL Audit Logs & Render Plotly Charts
```

---

## ☁️ Cloud Deployment

This application is ready for instant cloud deployment on **Streamlit Community Cloud**, **Render**, **Railway**, or **Heroku**.

- **Streamlit Community Cloud**: Connect your GitHub repository, specify `app.py` as the main file, and deploy!
- **Heroku / Render**: Pre-configured with `Procfile` (`web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`) and `.streamlit/config.toml`.

---

## 🖼️ Screenshots

| Authentication Screen | File Analytics & Charts |
| :---: | :---: |
| *(Add Login/Signup Screenshot)* | *(Add Dashboard Screenshot)* |

| Machine Learning Clustering | System Information Telemetry |
| :---: | :---: |
| *(Add ML IsolationForest Screenshot)* | *(Add Hardware Telemetry Screenshot)* |

---

## 🚀 Future Roadmap
- 📁 Directory & Local Folder Batch Scanner
- 📄 Automated PDF & Executive HTML Summary Reports
- 🧹 Automated One-Click Duplicate Cleanup & Archiving
- 🔒 AES-256 File Encryption Utilities

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).
