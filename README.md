# 🔑 Outlook Cookie Automation

<div align="center">

![Outlook](https://img.shields.io/badge/Outlook-0078D4?style=for-the-badge&logo=microsoft-outlook&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

</div>

## 📋 Description
Automated tool for capturing network requests and headers from Outlook's contact LinkedIn integration. Primary focus is on intercepting and logging network requests when accessing LinkedIn data through Outlook's contact feature.

## 🔧 Requirements

### System Requirements
- **Operating System:** Ubuntu 20.04 or later
- **Python Version:** 3.8 or later
- **Chrome Version:** 134.0 or later
- **ChromeDriver:** Compatible with installed Chrome version

### Dependencies
- selenium==4.11.2
- python-dotenv==1.0.0
- selenium-wire==5.1.0
- webdriver-manager==4.0.0

## ⚙️ Installation

1. **System Preparation:**
```bash
# Update system packages
sudo apt update
sudo apt upgrade

# Install Chrome (if not installed)
sudo apt install google-chrome-stable

# Install Python and pip
sudo apt install python3 python3-pip
```

2. **Create Virtual Environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

4. **Environment Setup:**
```bash
cp .env.example .env
# Edit .env with your credentials
```

## 🚀 Usage

1. **Configure Environment:**
   - Add your Outlook credentials to `.env`
   - Add target contact email
   - Verify Chrome and ChromeDriver versions match

2. **Run the Script:**
```bash
python main.py
```

## ⚠️ Important Notes

### Current Scope
- Primary focus is on capturing LinkedIn request headers from Outlook contacts
- Main functionality revolves around:
  - Outlook authentication
  - Contact access
  - Network request interception
  - Request header logging

### Known Limitations
1. Not handling all possible Outlook authentication scenarios
2. Limited error recovery for network issues
3. May require adjustments for different Outlook configurations
4. Authentication flow might vary based on account or other settings

### Future Improvements
- [ ] Handle multi-factor authentication
- [ ] Better session management
- [ ] Enhanced error recovery
- [ ] Support for different authentication methods
- [ ] Handle rate limiting and timeouts

## 📊 Output Files

- **Network Logs:** `network_logs_[timestamp].txt`
- **LinkedIn Requests:** `linkedin_requests.csv`

## 🤝 Contributing
Feel free to contribute by:
1. Forking the repository
2. Creating a feature branch
3. Committing changes
4. Opening a pull request

## ⚖️ License
This project is licensed under the MIT License - see the LICENSE file for details.

## 📝 Note
This tool is for educational purposes only. Ensure compliance with Microsoft's terms of service and your organization's policies.
