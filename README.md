# 🌐 Selenium Network Logger

<div align="center">

![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Chrome](https://img.shields.io/badge/Chrome-4285F4?style=for-the-badge&logo=google-chrome&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

</div>

## 📋 Description

An open-source Python library demonstrating advanced network traffic monitoring, Chrome DevTools Protocol (CDP) interception, HAR 1.2 exporting, and Pandas-powered analytics for Selenium WebDriver automation.

### Key Features
- 🔍 **Real-time CDP Network Monitoring**: Intercept requests and responses directly via Chrome DevTools Protocol.
- 📊 **HAR 1.2 Format Exporter**: Standardized network session exports compatible with BrowserMob, Charles, and Chrome DevTools.
- 📝 **CSV Summary Exporter**: Compact tabular exports of HTTP traffic.
- 📈 **Pandas Analytics Engine**: Convert raw network streams into DataFrames for fast status distribution & timing audits.
- 🚦 **CI/CD Quality Gates**: Easily fail automated builds on HTTP errors (>=400) or latency regressions.
- 🐳 **Docker Containerization**: Production-ready `Dockerfile` and `docker-compose.yml` pre-configured with Chromium & ChromeDriver.

---

## 📁 Project Architecture

```text
selenium-network-logger/
├── main.py                  # Core Runner Orchestrator
├── network_logger.py        # Central Engine (NetworkLogger)
├── chrome_monitor.py        # Chrome CDP & WebSocket Interface
├── har_exporter.py          # HAR 1.2 Format Generator & CSV Exporter
├── network_analyzer.py      # Pandas Analytics Engine
├── timing.py                # Performance Timing Helpers
├── Dockerfile               # Production Container Image
├── docker-compose.yml       # Docker Compose Configuration
├── requirements.txt      # Project Dependencies
└── examples/
    ├── basic_usage.py       # Connected Workflow Example
    ├── ci_pipeline.py       # CI/CD Quality Gate Example
    └── outlook_monitor.py   # Outlook Case Study Example
```

### Module Responsibilities

- **`network_logger.py`**: High-level `NetworkLogger` class coordinating Selenium WebDriver, CDP monitoring, and HAR/CSV exports.
- **`chrome_monitor.py`**: Manages `NetworkMonitor`, `WebSocketNetworkListener`, and `BrowserMonitorFactory`.
- **`har_exporter.py`**: Converts raw event JSON streams into standardized HAR 1.2 logs via `HARExporter` & exports CSV via `CSVExporter`.
- **`network_analyzer.py`**: Aggregates HAR data into Pandas DataFrames using `NetworkAnalyzer`.
- **`main.py`**: Top-level application runner importing reusable workflows.

---

## ⚙️ Setup & Installation

1. **Clone Repository**:
```bash
git clone https://github.com/DevAsadYasin/selenium-network-logger.git
cd selenium-network-logger
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage Examples

### 1. Main Core Runner
Run all connected workflows:
```bash
python main.py
```

### 2. Basic Connected Workflow
Run the basic usage example script:
```bash
python examples/basic_usage.py
```

### 3. Quick Code Example
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from network_logger import NetworkLogger

# 1. Enable Performance Logging in Chrome
options = Options()
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
driver = webdriver.Chrome(options=options)

try:
    # 2. Attach NetworkLogger
    logger = NetworkLogger(driver)
    logger.start()

    # 3. Perform Automation
    driver.get("https://example.com")
    logger.capture_logs()

    # 4. Export Reports
    logger.export_har("network.har")
    logger.export_csv("network.csv")

    # 5. Pandas Analytics
    df = logger.get_dataframe()
    print(df.head())

finally:
    driver.quit()
```

### 4. CI/CD Quality Gate
Run the automated CI build script:
```bash
python examples/ci_pipeline.py
```

### 5. Case Study: Outlook & LinkedIn Header Extraction
Run the Microsoft Outlook background API header extraction case study:
```bash
python examples/outlook_monitor.py
```

---

## 🐳 Docker Deployment

Run the solution in a isolated container environment without installing local Chrome drivers:

```bash
docker compose up --build
```

---

## 📜 License

MIT License - See LICENSE file for details.
