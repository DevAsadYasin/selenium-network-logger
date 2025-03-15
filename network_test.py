# Description: Test network request capturing using Selenium and Chrome DevTools Protocol (CDP)
# Dependencies: selenium, python-dotenv
# Usage: python network_test.py
# Note: Make sure to update the TEST_BASE_URL and TEST_PRICING_URL with your desired URLs
# Note: This script will save network logs to a file named test_network_logs_<timestamp>.txt
# Note: You need to have Chrome installed on your system
# Note: You need to have the ChromeDriver installed on your system
# Note: You need to have the .env file with the required environment variables

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
from datetime import datetime
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

load_dotenv()

TEST_BASE_URL = os.getenv('TEST_BASE_URL', 'https://anything.com')
TEST_PRICING_URL = os.getenv('TEST_PRICING_URL', 'https://anything.com/anything')

def get_log_filepath():
    """Get filepath for network logs"""
    base_dir = "/home/dev/outlook-cookie-automation"
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"test_network_logs_{timestamp}.txt"
    return os.path.join(base_dir, filename)

def log_request(request_data, log_file):
    """Log request details to file"""
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write("\n" + "="*80 + "\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"URL: {request_data.get('url')}\n")
            f.write(f"Method: {request_data.get('method')}\n")
            f.write("Headers:\n")
            for key, value in request_data.get('headers', {}).items():
                f.write(f"{key}: {value}\n")
            f.write("="*80 + "\n")
        print(f"Logged request: {request_data.get('url')}")
    except Exception as e:
        print(f"Error logging request: {str(e)}")

def setup_network_monitoring():
    """Setup Chrome with network monitoring"""
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--enable-automation')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.set_capability(
        "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
    )
    
    service = Service('/usr/lib/chromium-browser/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.set_page_load_timeout(30)
    
    driver.captured_requests = []
    driver.log_file = get_log_filepath()
    print(f"Network logs will be saved to: {driver.log_file}")
    
    driver.execute_cdp_cmd('Network.enable', {})
    driver.execute_cdp_cmd('Page.enable', {})
    
    return driver

def wait_for_page_load(driver, url, timeout=30):
    """Wait for page to load with better error handling"""
    try:
        print(f"\nNavigating to: {url}")
        driver.get(url)
        
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        print(f"Successfully loaded: {url}")
        return True
    except Exception as e:
        print(f"Error loading page: {str(e)}")
        return False

def get_performance_logs(driver):
    """Extract network requests from performance logs"""
    try:
        logs = driver.get_log('performance')
        for entry in logs:
            try:
                data = json.loads(entry['message'])['message']
                if (
                    'Network.requestWillBeSent' == data['method']
                    and data.get('params', {}).get('request')
                ):
                    request = data['params']['request']
                    log_request(request, driver.log_file)
                    driver.captured_requests.append(request)
            except:
                continue
    except Exception as e:
        print(f"Error getting performance logs: {str(e)}")

def test_network_capture():
    """Test network request capturing"""
    driver = None
    try:
        print("Starting network capture test...")
        driver = setup_network_monitoring()
        
        print(f"\nTesting homepage: {TEST_BASE_URL}")
        if wait_for_page_load(driver, TEST_BASE_URL):
            time.sleep(3)
            get_performance_logs(driver)
            print(f"Captured {len(driver.captured_requests)} requests")
        
        print(f"\nTesting pricing page: {TEST_PRICING_URL}")
        if wait_for_page_load(driver, TEST_PRICING_URL):
            time.sleep(3)
            get_performance_logs(driver)
            print(f"Total captured requests: {len(driver.captured_requests)}")
        
        print(f"\nAll requests have been logged to: {driver.log_file}")
        
    except Exception as e:
        print(f"Test error: {str(e)}")
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

if __name__ == "__main__":
    test_network_capture()
