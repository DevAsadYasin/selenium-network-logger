import json
import requests
import websocket
from typing import Dict, List, Optional


class NetworkMonitor:
    """Manages Chrome DevTools Protocol (CDP) connection via ChromeDriver's JSON debugging port."""

    def __init__(self, driver):
        self.driver = driver
        self.websocket_url = self._get_websocket_debugger_url()

    def _get_websocket_debugger_url(self) -> Optional[str]:
        """Fetch the WebSocket debugger URL from ChromeDriver's HTTP endpoint."""
        try:
            port = getattr(self.driver.service, 'port', None)
            if not port:
                return None
            debugger_url = f"http://localhost:{port}/json"
            response = requests.get(debugger_url, timeout=5)
            tabs = response.json()
            if isinstance(tabs, list):
                for tab in tabs:
                    if isinstance(tab, dict) and tab.get('type') == 'page' and 'webSocketDebuggerUrl' in tab:
                        return tab['webSocketDebuggerUrl']
                for tab in tabs:
                    if isinstance(tab, dict) and 'webSocketDebuggerUrl' in tab:
                        return tab['webSocketDebuggerUrl']
            elif isinstance(tabs, dict) and 'webSocketDebuggerUrl' in tabs:
                return tabs['webSocketDebuggerUrl']
        except Exception as e:
            print(f"Warning: Could not fetch WebSocket debugger URL: {e}")
        return None

    def enable_network(self):
        """Enable network monitoring via Selenium CDP command."""
        self.driver.execute_cdp_cmd("Network.enable", {})
        self.driver.execute_cdp_cmd("Page.enable", {})


class WebSocketNetworkListener:
    """Listens for real-time CDP network events over a WebSocket connection."""

    def __init__(self, websocket_url: str):
        self.websocket_url = websocket_url
        self.network_events: List[Dict] = []
        self.ws: Optional[websocket.WebSocketApp] = None

    def on_message(self, ws, message):
        data = json.loads(message)
        if data.get('method', '').startswith('Network.'):
            self.network_events.append(data)

    def start_listening(self):
        """Start listening on the WebSocket connection."""
        def on_open(ws):
            ws.send(json.dumps({
                "id": 1,
                "method": "Network.enable",
                "params": {}
            }))

        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(
            self.websocket_url,
            on_message=self.on_message,
            on_open=on_open
        )
        self.ws.run_forever()


class ChromeNetworkMonitor(NetworkMonitor):
    """Chrome-specific implementation of network monitoring."""
    pass


class BrowserMonitorFactory:
    """Factory for creating browser-specific network monitors."""

    @staticmethod
    def create_monitor(driver) -> NetworkMonitor:
        browser = driver.capabilities.get('browserName', '').lower()
        if browser == 'chrome':
            return ChromeNetworkMonitor(driver)
        else:
            return NetworkMonitor(driver)
