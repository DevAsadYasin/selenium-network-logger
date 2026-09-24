from typing import Dict, Any


def calculate_request_timing(request_sent_event: Dict[str, Any], response_received_event: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate latency and duration from CDP timestamps."""
    start_time = request_sent_event.get("params", {}).get("timestamp", 0)
    end_time = response_received_event.get("params", {}).get("timestamp", 0)
    duration_ms = max(0, (end_time - start_time) * 1000)

    response_info = response_received_event.get("params", {}).get("response", {})
    return {
        "url": response_info.get("url", ""),
        "status": response_info.get("status", 0),
        "duration_ms": round(duration_ms, 2),
        "mime_type": response_info.get("mimeType", "")
    }
