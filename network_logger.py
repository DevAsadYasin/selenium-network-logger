import json
import pandas as pd
from typing import Dict, Any, Optional
from chrome_monitor import NetworkMonitor
from har_exporter import HARExporter, CSVExporter
from network_analyzer import NetworkAnalyzer


class NetworkLogger:
    """Central orchestrator connecting Selenium WebDriver with CDP monitoring and HAR export."""

    def __init__(self, driver):
        self.driver = driver
        self.monitor = NetworkMonitor(driver)
        self.exporter = HARExporter()
        self.captured_events = []

    def start(self):
        """Enable CDP Network and Page domain events."""
        self.driver.execute_cdp_cmd('Network.enable', {})
        self.driver.execute_cdp_cmd('Page.enable', {})

    def capture_logs(self):
        """Extract CDP performance events from driver performance logs and record them in HAR exporter."""
        try:
            logs = self.driver.get_log('performance')
            for entry in logs:
                message = json.loads(entry['message'])['message']
                method = message.get('method', '')
                if method.startswith('Network.'):
                    self.captured_events.append(message)
                    if method == 'Network.responseReceived':
                        params = message.get('params', {})
                        response = params.get('response', {})
                        request_data = {'url': response.get('url', ''), 'method': 'GET', 'headers': response.get('headers', {})}
                        response_data = {'status': response.get('status', 200), 'headers': response.get('headers', {}), 'mimeType': response.get('mimeType', '')}
                        timing_data = {'duration': response.get('timing', {}).get('receiveHeadersEnd', 0)}
                        self.exporter.add_network_entry(request_data, response_data, timing_data)
        except Exception as e:
            print(f"Warning capturing logs: {e}")

    def export_har(self, filepath: str = "network_log.har") -> Dict[str, Any]:
        """Save HAR output to a JSON file."""
        return self.exporter.save(filepath)

    def export_csv(self, filepath: str = "network_log.csv"):
        """Save network entries summary to a CSV file."""
        entries = self.exporter.har_structure["log"]["entries"]
        CSVExporter.export_network_data(entries, filepath)

    def analyze(self) -> NetworkAnalyzer:
        """Create a NetworkAnalyzer instance from collected HAR data."""
        har_data = self.exporter.get_har_dict()
        return NetworkAnalyzer(har_data)

    def get_dataframe(self) -> pd.DataFrame:
        """Get network data directly as a Pandas DataFrame."""
        return self.analyze().df
