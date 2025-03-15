# 🌐 Selenium Network Request Capture

<div align="center">

![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Chrome](https://img.shields.io/badge/Chrome-4285F4?style=for-the-badge&logo=google-chrome&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

</div>

## 📋 Description

A Python-Selenium based tool demonstrating advanced network request capturing and monitoring capabilities. Uses Chrome DevTools Protocol (CDP) to intercept and log network requests in web applications.

### Key Features
- 🔍 Real-time network request monitoring
- 📝 Comprehensive request logging
- 🎯 Request header extraction
- 💾 CSV and TXT output formats
- 🚦 Traffic analysis capabilities

## 🎯 Primary Focus

1. **Network Request Capture:**
   - Real-time request interception
   - Header extraction and parsing
   - URL pattern matching
   - Request method identification

2. **Selenium Automation:**
   - Chrome DevTools Protocol integration
   - Performance log monitoring
   - Network traffic analysis
   - Request filtering capabilities

3. **Data Collection:**
   - Structured logging
   - CSV export functionality
   - Request header analysis
   - URL pattern monitoring

## 🔧 Technical Implementation

### Network Monitoring
```python
driver.execute_cdp_cmd('Network.enable', {})
driver.execute_cdp_cmd('Page.enable', {})
```

### Request Capture
```python
logs = driver.get_log('performance')
for entry in logs:
    data = json.loads(entry['message'])['message']
    if 'Network.requestWillBeSent' == data['method']:
        # Process request...
```

## 📊 Example Implementation

The repository includes a practical implementation using Microsoft Outlook as an example:
- Demonstrates network request capture in a real-world application
- Shows how to extract specific request patterns (LinkedIn integration)
- Provides logging and data extraction examples

### Test Implementation
- Separate test script (`network_test.py`)
- Basic URL request capture
- Header logging demonstration
- Pattern matching example

## 🔧 Requirements

### System Requirements
- **OS:** Ubuntu 20.04+
- **Python:** 3.8+
- **Chrome:** 134.0+
- **ChromeDriver:** Compatible version

### Python Dependencies
```text
selenium==4.11.2
python-dotenv==1.0.0
selenium-wire==5.1.0
webdriver-manager==4.0.0
```

## ⚙️ Setup & Usage

1. **Environment Setup:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. **Configuration:**
```bash
cp .env.example .env
# Configure environment variables
```

3. **Test Network Capture:**
```bash
python network_test.py
```

4. **Run Example Implementation:**
```bash
python main.py
```

## 📊 Output Files

### Network Logs (TXT)
- Timestamp
- Request URL
- Method
- Headers
- Request body (if applicable)

### Filtered Requests (CSV)
- Timestamp
- Target URL
- Complete headers
- Pattern matches

## 🤝 Contributing

Areas for improvement:
- Additional request capture methods
- Enhanced pattern matching
- Better error handling
- More export formats
- Extended CDP integration

## ⚠️ Disclaimer

This tool is for educational purposes, demonstrating Selenium's network monitoring capabilities. Example implementation with Outlook is for demonstration only.

## 📜 License

MIT License - See LICENSE file for details.
