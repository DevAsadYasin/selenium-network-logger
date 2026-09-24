import os
import sys
import time
import json
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Ensure parent directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from network_logger import NetworkLogger
from config import URLS, generate_random_name, CONTACT_EMAIL, OUTLOOK_EMAIL, OUTLOOK_PASSWORD


def get_log_filepath():
    """Get filepath for the network log file"""
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    os.makedirs(base_dir, exist_ok=True)
    filename = f"network_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    return os.path.join(base_dir, filename)


def get_csv_filepath():
    """Get filepath for the CSV file"""
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    os.makedirs(base_dir, exist_ok=True)
    filename = "linkedin_requests.csv"
    return os.path.join(base_dir, filename)


def save_request_headers_to_csv(email, headers, url):
    """Save request headers to CSV file with proper file handling"""
    try:
        filepath = get_csv_filepath()
        file_exists = os.path.exists(filepath)
        mode = 'a' if file_exists else 'w'
        write_header = not file_exists
        
        with open(filepath, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if write_header:
                writer.writerow(['Timestamp', 'Email', 'URL', 'Headers'])
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([
                timestamp,
                email,
                url,
                '\n'.join([f"{k}: {v}" for k, v in headers.items()])
            ])
            
        print(f"\nSaved LinkedIn Request to CSV: {filepath}")
        return True
    except Exception as e:
        print(f"Error saving headers to CSV: {str(e)}")
        return False


def enter_email(driver, email):
    """Enter email and submit"""
    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "loginfmt"))
        )
        time.sleep(1.5)
        email_input.clear()
        for char in email:
            email_input.send_keys(char)
            time.sleep(0.05)
        
        time.sleep(1)
        next_button = driver.find_element(By.ID, "idSIButton9")
        next_button.click()
        print("Email entered successfully")
        return True
    except Exception as e:
        print(f"Error entering email: {str(e)}")
        return False


def enter_password(driver, password):
    """Enter password and submit"""
    try:
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "passwd"))
        )
        time.sleep(1.5)
        password_input.clear()
        for char in password:
            password_input.send_keys(char)
            time.sleep(0.05)
        
        time.sleep(1)
        sign_in_button = driver.find_element(By.ID, "idSIButton9")
        sign_in_button.click()
        print("Sign in button clicked")
        time.sleep(3)
        return True
    except Exception as e:
        print(f"Error entering password: {str(e)}")
        return False


def handle_stay_signed_in(driver):
    """Handle the 'Stay signed in?' dialog"""
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "kmsiTitle"))
        )
        yes_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"][aria-label="Yes"][id="acceptButton"]'))
        )
        time.sleep(1)
        yes_button.click()
        print("Clicked 'Yes' on stay signed in dialog")
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Error handling stay signed in dialog: {str(e)}")
        return False


def run_outlook_example():
    """Outlook specific network monitoring workflow."""
    print("Starting Outlook Network Monitoring Example...")
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Attach NetworkLogger
        logger = NetworkLogger(driver)
        logger.start()

        driver.get(URLS['login'])
        print(f"Navigated to: {URLS['login']}")

        if OUTLOOK_EMAIL and OUTLOOK_PASSWORD:
            enter_email(driver, OUTLOOK_EMAIL)
            enter_password(driver, OUTLOOK_PASSWORD)
            handle_stay_signed_in(driver)

        # Capture traffic and export logs
        logger.capture_logs()
        logger.export_har("outlook_session.har")
        logger.export_csv("outlook_session.csv")
        print("Outlook Session Network Logs Exported Successfully.")

    finally:
        driver.quit()


if __name__ == "__main__":
    run_outlook_example()
