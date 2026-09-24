import os
import sys

# Ensure parent directory is in path when running directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from network_logger import NetworkLogger


def run_ci_network_test():
    """CI/CD Quality Gate Example Script."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Attach NetworkLogger to Driver
        logger = NetworkLogger(driver)
        logger.start()

        # Perform Automated Browsing Actions
        print("Navigating to target URL in CI...")
        driver.get("https://httpbin.org/status/200")

        # Extract Traffic & Export Reports
        logger.capture_logs()
        logger.export_har("ci_build.har")
        logger.export_csv("ci_build.csv")

        # Analyze Results via Pandas
        df = logger.get_dataframe()

        # Check for HTTP Failures (Status >= 400)
        failed_requests = df[df['status'] >= 400]
        if not failed_requests.empty:
            print(f"❌ CI Build Failed: {len(failed_requests)} network request(s) failed!")
            print(failed_requests[['url', 'status', 'time']])
            sys.exit(1)

        print("✅ CI Network Quality Gate Passed successfully!")

    finally:
        driver.quit()


if __name__ == "__main__":
    run_ci_network_test()
