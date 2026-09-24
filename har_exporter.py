import csv
import json
from datetime import datetime, timezone
from typing import Dict, List, Any


class HARExporter:
    """Formats captured network request/response events into standard HAR 1.2 format."""

    def __init__(self, creator_name: str = "Selenium Network Logger", creator_version: str = "1.0"):
        self.har_structure: Dict[str, Any] = {
            "log": {
                "version": "1.2",
                "creator": {
                    "name": creator_name,
                    "version": creator_version
                },
                "entries": []
            }
        }

    def _format_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format request details into HAR request object."""
        headers = [
            {"name": k, "value": str(v)}
            for k, v in request_data.get("headers", {}).items()
        ]
        return {
            "method": request_data.get("method", "GET"),
            "url": request_data.get("url", ""),
            "httpVersion": request_data.get("protocol", "HTTP/1.1"),
            "headers": headers,
            "queryString": [],
            "cookies": [],
            "headersSize": -1,
            "bodySize": request_data.get("postDataEntries", 0)
        }

    def _format_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format response details into HAR response object."""
        headers = [
            {"name": k, "value": str(v)}
            for k, v in response_data.get("headers", {}).items()
        ]
        return {
            "status": response_data.get("status", 200),
            "statusText": response_data.get("statusText", "OK"),
            "httpVersion": response_data.get("protocol", "HTTP/1.1"),
            "headers": headers,
            "cookies": [],
            "content": {
                "size": response_data.get("encodedDataLength", 0),
                "mimeType": response_data.get("mimeType", "text/html")
            },
            "redirectURL": "",
            "headersSize": -1,
            "bodySize": response_data.get("encodedDataLength", 0)
        }

    def add_network_entry(self, request_data: Dict[str, Any], response_data: Dict[str, Any], timing_data: Dict[str, Any]):
        """Add a formatted network entry into HAR structure."""
        entry = {
            "startedDateTime": datetime.now(timezone.utc).isoformat(),
            "time": timing_data.get('duration', 0),
            "request": self._format_request(request_data),
            "response": self._format_response(response_data),
            "timings": timing_data
        }
        self.har_structure["log"]["entries"].append(entry)

    def save(self, filename: str) -> Dict[str, Any]:
        """Save HAR structure to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.har_structure, f, indent=2)
        return self.har_structure

    def get_har_dict(self) -> Dict[str, Any]:
        """Get the complete HAR dictionary structure."""
        return self.har_structure


class CSVExporter:
    """Exports structured network entries to CSV format."""

    @staticmethod
    def export_network_data(network_entries: List[Dict[str, Any]], filename: str):
        """Export network entries to a CSV file."""
        fieldnames = [
            'timestamp', 'url', 'method', 'status_code',
            'response_time', 'content_length'
        ]
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in network_entries:
                writer.writerow({
                    'timestamp': entry.get('startedDateTime', ''),
                    'url': entry['request'].get('url', ''),
                    'method': entry['request'].get('method', ''),
                    'status_code': entry['response'].get('status', 0),
                    'response_time': entry.get('time', 0),
                    'content_length': entry['response']['content'].get('size', 0)
                })
