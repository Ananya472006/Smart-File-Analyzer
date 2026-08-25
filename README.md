# Smart File Analyzer

## Overview
**Smart File Analyzer** is a functional, feature-packed Streamlit application designed for multi-file metadata extraction, file type classification, cryptographic duplicate detection via SHA-256 hashing, storage distribution analysis, and live system hardware telemetry.

---

## Features
- **Multi-File Upload**: Upload multiple files of any type (`.csv`, `.xlsx`, `.pdf`, `.txt`, `.docx`, images, `.zip`, `.json`, `.py`, etc.).
- **File Metadata Analysis**: Computes file name, extension, category, size in bytes/KB/MB, and SHA-256 hash.
- **File Type Classification**: Automatically groups files into general categories (Documents, Images, Videos, Audio, Archives, Data, Code, Other).
- **Duplicate Detection**: Identifies exact duplicate files using SHA-256 cryptographic hashing.
- **Largest Files Ranking**: Displays top 10 largest uploaded files sorted from largest to smallest.
- **Interactive Visualizations**: Dynamic **Plotly** bar charts for file type counts, total storage distribution, and top largest file comparisons.
- **Interactive Filtering**: Filter files by category, minimum size, and maximum size.
- **System Information Page**: Real-time telemetry displaying host Operating System, CPU cores & usage, RAM usage, and Disk space.

---

## Technologies
- **Python 3**
- **Streamlit**
- **Pandas**
- **Plotly**
- **psutil**
- **hashlib**

---

## Project Structure
```
Smart-File-Analyzer/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── utils/
│   ├── __init__.py
│   ├── file_analyzer.py
│   └── system_info.py
│
└── assets/
    └── .gitkeep
```

---

## Installation & Setup

1. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   ```

2. **Activate Virtual Environment**
   - **Windows:**
     ```cmd
     venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

---

## How It Works
```
Upload Files
     ↓
Process Metadata & SHA-256
     ↓
Analyze Categories & Sizes
     ↓
Detect Duplicates & Top Files
     ↓
Generate Interactive Charts
```

---

## System Information
The mandatory **System Information** page reads live telemetry from the machine hosting the Streamlit server using `platform` and `psutil` libraries. It displays real-time CPU usage, RAM utilization, and disk partition stats.

---

## Screenshots
*(Placeholder section for application screenshots)*

---

## Future Improvements
- Folder scanning capabilities
- Automated file cleanup suggestions
- PDF/CSV report exports
- Deep content inspection for text files
