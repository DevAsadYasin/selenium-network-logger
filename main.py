from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import URLS, generate_random_name, CONTACT_EMAIL, OUTLOOK_EMAIL, OUTLOOK_PASSWORD
import csv
from datetime import datetime
import os
import json

def get_log_filepath():
    """Get filepath for the network log file"""
    base_dir = "/home/dev/outlook-cookie-automation"
    filename = f"network_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    return os.path.join(base_dir, filename)

def log_network_request(request_data, log_file):
    """Log network request to file"""
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"URL: {request_data.get('url', 'N/A')}\n")
            f.write(f"Method: {request_data.get('method', 'N/A')}\n")
            f.write("Headers:\n")
            for k, v in request_data.get('headers', {}).items():
                f.write(f"{k}: {v}\n")
            f.write(f"{'='*50}\n")
    except Exception as e:
        print(f"Error logging request: {str(e)}")

def setup_chrome_driver():
    """Setup Chrome with network monitoring"""
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--enable-automation')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.set_capability(
        "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
    )
    
    try:
        service = Service('/usr/lib/chromium-browser/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.set_page_load_timeout(30)
        driver.captured_requests = []
        driver.network_log_file = get_log_filepath()
        
        driver.execute_cdp_cmd('Network.enable', {})
        driver.execute_cdp_cmd('Page.enable', {})
        
        print(f"Network logs will be saved to: {driver.network_log_file}")
        return driver
        
    except Exception as e:
        print(f"Failed to initialize ChromeDriver: {str(e)}")
        raise

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
                    log_network_request(request, driver.network_log_file)
                    
                    if 'linkedin/profiles/full' in request.get('url', ''):
                        print(f"\nCaptured LinkedIn request: {request['url']}")
                        driver.captured_requests.append(request)
            except:
                continue
    except Exception as e:
        print(f"Error getting performance logs: {str(e)}")

def capture_linkedin_request(driver, timeout=30):
    """Capture LinkedIn API request headers"""
    try:
        print("\nWaiting for LinkedIn request...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            for request in driver.captured_requests:
                if 'linkedin/profiles/full' in request.get('url', ''):
                    print(f"Found LinkedIn request: {request['url']}")
                    return request.get('headers', {}), request.get('url', '')
            time.sleep(0.5)
        
        print("No LinkedIn request captured within timeout period")
        return None, None
        
    except Exception as e:
        print(f"Error capturing request: {str(e)}")
        return None, None

def get_csv_filepath():
    """Get filepath for the CSV file"""
    # Update base directory as needed
    base_dir = "/home/dev/outlook-cookie-automation"
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
            
        print(f"\nSaved to CSV:")
        print(f"- File: {filepath}")
        print(f"- Timestamp: {timestamp}")
        print(f"- Email: {email}")
        print(f"- URL: {url}")
        return True
        
    except Exception as e:
        print(f"Error saving headers to CSV: {str(e)}")
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            print("Created directory structure")
            return save_request_headers_to_csv(email, headers, url)
        except Exception as dir_error:
            print(f"Error creating directory: {str(dir_error)}")
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
            time.sleep(0.5)
        
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
        
        time.sleep(2.5)
        
        password_input.clear()
        for char in password:
            password_input.send_keys(char)
            time.sleep(0.5)
        
        time.sleep(2)
        
        sign_in_button = driver.find_element(By.ID, "idSIButton9")
        sign_in_button.click()
        print("Sign in button clicked")
        
        time.sleep(3.5)
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
        print("Stay signed in dialog detected")
        
        yes_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"][aria-label="Yes"][id="acceptButton"]'))
        )
        
        time.sleep(2)
        yes_button.click()
        print("Clicked 'Yes' on stay signed in dialog")
        
        time.sleep(3)
        return True
        
    except Exception as e:
        print(f"Error handling stay signed in dialog: {str(e)}")
        return False

def wait_for_successful_login(driver):
    """Wait for successful login redirect"""
    try:
        WebDriverWait(driver, 20).until(
            lambda x: any(domain in x.current_url for domain in [
                "m365.cloud.microsoft",
                "www.office.com",
                "outlook.office.com",
                "outlook.office365.com"
            ])
        )
        print(f"Successfully logged in. Current URL: {driver.current_url}")
        return True
    except Exception as e:
        print(f"Error waiting for login redirect: {str(e)}")
        return False

def create_new_contact(driver):
    """Handle creating a new contact"""
    try:
        new_contact_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, 
                'button[data-automation-type="RibbonSplitButton"][aria-label="New contact"]'
            ))
        )
        time.sleep(2)
        new_contact_button.click()
        print("Clicked New Contact button")
        
        time.sleep(3)
        
        first_name, last_name = generate_random_name()
        
        first_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 
                'input[data-automation="Name.firstName"]'
            ))
        )
        time.sleep(1.5)
        for char in first_name:
            first_name_input.send_keys(char)
            time.sleep(0.12)
        
        time.sleep(1)
        
        last_name_input = driver.find_element(
            By.CSS_SELECTOR, 
            'input[data-automation="Name.lastName"]'
        )
        for char in last_name:
            last_name_input.send_keys(char)
            time.sleep(0.12)
        
        time.sleep(1.5)
        
        email_input = driver.find_element(
            By.CSS_SELECTOR, 
            'input[data-automation="Email.email1"]'
        )
        for char in CONTACT_EMAIL:
            email_input.send_keys(char)
            time.sleep(0.1)
        
        time.sleep(2)
        
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, 
                'button[data-automation="LPESave"]'
            ))
        )
        time.sleep(1)
        save_button.click()
        print(f"Created contact: {first_name} {last_name}")
        
        return True
    except Exception as e:
        print(f"Error creating contact: {str(e)}")
        return False

def find_and_click_contact(driver, email_to_find):
    """Find and click on a specific contact"""
    try:
        contact_selector = f"div[aria-label*='{email_to_find}']"
        contact = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, contact_selector))
        )
        
        time.sleep(2)
        contact.click()
        print(f"Found and clicked contact with email: {email_to_find}")
        return True
    except Exception as e:
        print(f"Error finding contact: {str(e)}")
        return False

def capture_network_requests(driver):
    """Capture network requests from performance logs"""
    try:
        requests = []
        # Get performance logs and extract network requests
        logs = driver.get_log('performance')
        for entry in logs:
            try:
                # Parse log entry and extract network request data if available
                data = json.loads(entry['message'])['message']
                if (
                    'Network.requestWillBeSent' == data['method']
                    and data.get('params', {}).get('request')
                ):
                    request = data['params']['request']
                    requests.append(request)
                    # Log request to file for debugging purposes
                    log_network_request(request, driver.network_log_file)
            except:
                continue
        # Return all captured requests for further processing
        return requests
    except Exception as e:
        print(f"Error capturing network requests: {str(e)}")
        return []

def find_linkedin_request(captured_requests):
    """Find LinkedIn profile request in captured requests"""
    for request in captured_requests:
        if 'linkedin/profiles/full' in request.get('url', ''):
            print(f"\nFound LinkedIn request URL: {request['url']}")
            return request
    return None

def click_linkedin_tab(driver):
    """Click LinkedIn tab and process captured requests"""
    try:
        # Start capturing network requests before clicking LinkedIn tab
        driver.captured_requests = []
        print("\nStarted monitoring network requests...")
        
        # Find LinkedIn button and click it
        linkedin_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, 
                "button[name='LinkedIn'][role='tab']"
            ))
        )
        
        print("Found LinkedIn button, clicking...")
        linkedin_button.click()
        
        # Wait for requests to complete before processing
        time.sleep(5)
        
        # Capture all requests
        all_requests = capture_network_requests(driver)
        print(f"Captured {len(all_requests)} network requests")
        
        # Find LinkedIn request from captured requests
        linkedin_request = find_linkedin_request(all_requests)
        
        if linkedin_request:
            # Save to CSV if found
            if save_request_headers_to_csv(
                CONTACT_EMAIL,
                linkedin_request.get('headers', {}),
                linkedin_request.get('url', '')
            ):
                print("Successfully saved LinkedIn request data")
            else:
                print("Failed to save LinkedIn request data")
        else:
            print("No LinkedIn profile request found in captured requests")
        
        return True
    except Exception as e:
        print(f"Error in LinkedIn tab handling: {str(e)}")
        return False

def check_contact_exists(driver, email_to_find):
    """Check if contact already exists"""
    try:
        time.sleep(3)
        
        contact_selector = f"div[aria-label*='{email_to_find}']"
        try:
            contact = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, contact_selector))
            )
            print(f"Contact found with email: {email_to_find}")
            return True
        except:
            print(f"Contact not found with email: {email_to_find}")
            return False
            
    except Exception as e:
        print(f"Error checking for contact: {str(e)}")
        return False

def handle_people_page(driver, email):
    """Open and handle People page in new tab"""
    try:
        time.sleep(6)
        print("Starting network capture for People page...")
        driver.captured_requests = []
        
        original_window = driver.current_window_handle
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                driver.execute_script("window.open('about:blank', '_blank');")
                time.sleep(2)
                
                new_window = [handle for handle in driver.window_handles if handle != original_window][0]
                driver.switch_to.window(new_window)
                
                driver.get(URLS['people'])
                print("Successfully navigated to People page")
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(3)
        
        time.sleep(10)
        
        try:
            email_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, "loginfmt"))
            )
            email_input.clear()
            email_input.send_keys(email)
            sign_in_button = driver.find_element(By.ID, "idSIButton9")
            sign_in_button.click()
            print("Signed in on People page")
            time.sleep(5)
        except:
            print("No need to sign in again, already authenticated")
        
        contact_exists = check_contact_exists(driver, CONTACT_EMAIL)
        
        if not contact_exists:
            print("Contact doesn't exist, creating new contact...")
            for attempt in range(3):
                try:
                    new_contact_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-automationid="splitbuttonprimary"]'))
                    )
                    time.sleep(2)
                    new_contact_button.click()
                    print("Clicked New contact button")
                    break
                except:
                    print(f"Attempt {attempt + 1} to click New contact button failed")
                    if attempt == 2:
                        raise
                    time.sleep(5)
            
            if not create_new_contact(driver):
                raise Exception("Failed to create new contact")
            
            time.sleep(5)
        else:
            print("Contact already exists, proceeding to click...")
        
        if not find_and_click_contact(driver, CONTACT_EMAIL):
            raise Exception("Failed to find and click contact")
            
        time.sleep(3)
        print(f"Total requests captured so far: {len(driver.captured_requests)}")
        
        # Enable performance logging before clicking LinkedIn tab
        # This starts capturing network requests
        
        driver.execute_cdp_cmd('Network.enable', {})
        print("Network monitoring enabled")
        
        if not click_linkedin_tab(driver):
            raise Exception("Failed to click LinkedIn tab")
        
        print("Waiting 15 seconds to see the result...")
        time.sleep(15)
        return True
        
    except Exception as e:
        print(f"Error handling People page: {str(e)}")
        try:
            driver.switch_to.window(original_window)
        except:
            pass
        return False

def login_sequence(driver, email, password):
    """Complete full login sequence"""
    try:
        if not enter_email(driver, email):
            raise Exception("Failed to enter email")
        
        time.sleep(3)
        print("Proceeding to password entry...")
        
        if not enter_password(driver, password):
            raise Exception("Failed to enter password")
        
        if not handle_stay_signed_in(driver):
            raise Exception("Failed to handle stay signed in dialog")
        
        if not wait_for_successful_login(driver):
            raise Exception("Failed to confirm successful login")
        
        time.sleep(5)
        
        if not handle_people_page(driver, email):
            raise Exception("Failed to handle People page")
        
        return True
        
    except Exception as e:
        print(f"Login sequence failed: {str(e)}")
        return False

def main():
    try:
        driver = setup_chrome_driver()
        
        driver.get(URLS['login'])
        print("Navigated to login page")
        time.sleep(2)
        
        if not login_sequence(driver, OUTLOOK_EMAIL, OUTLOOK_PASSWORD):
            raise Exception("Login sequence failed")
        
        time.sleep(15)
        print("Sequence completed")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        time.sleep(10)
        driver.quit()

if __name__ == "__main__":
    main()
