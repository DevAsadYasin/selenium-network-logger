import os
import sys

# Ensure parent directory is in path when running directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from network_logger import NetworkLogger


def run_connected_example():
    """Basic usage example of Selenium Network Logger."""
    print("Setting up Chrome driver with performance logging enabled...")
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Initialize and start Network Logger
        logger = NetworkLogger(driver)
        logger.start()

        # Perform navigation
        target_url = "https://httpbin.org/get"
        print(f"Navigating to: {target_url}")
        driver.get(target_url)

        # Capture and export logs
        logger.capture_logs()
        har_file = "output.har"
        csv_file = "output.csv"
        logger.export_har(har_file)
        logger.export_csv(csv_file)
        print(f"Exported HAR to '{har_file}' and CSV to '{csv_file}'.")

        # Perform Pandas Analytics
        df = logger.get_dataframe()
        print("\n--- Captured Network Requests DataFrame ---")
        print(df)

        analyzer = logger.analyze()
        print("\n--- Network Analytics Summary ---")
        print(analyzer.get_summary())

    finally:
        driver.quit()


if __name__ == "__main__":
    run_connected_example()
