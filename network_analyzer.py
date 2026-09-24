import pandas as pd
from typing import Dict, Any


class NetworkAnalyzer:
    """Analyzes HAR data using Pandas DataFrames."""

    def __init__(self, har_data: Dict[str, Any]):
        self.df = self._har_to_dataframe(har_data)

    def _har_to_dataframe(self, har_data: Dict[str, Any]) -> pd.DataFrame:
        """Convert HAR JSON data into a structured Pandas DataFrame."""
        entries = har_data.get('log', {}).get('entries', [])
        flattened_data = []
        for entry in entries:
            req = entry.get('request', {})
            res = entry.get('response', {})
            content = res.get('content', {})
            flattened_data.append({
                'url': req.get('url', ''),
                'method': req.get('method', ''),
                'status': res.get('status', 0),
                'time': entry.get('time', 0),
                'size': content.get('size', 0),
                'mime_type': content.get('mimeType', '')
            })
        return pd.DataFrame(flattened_data)

    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics of network requests."""
        if self.df.empty:
            return {"total_requests": 0, "failed_requests": 0}
        return {
            "total_requests": len(self.df),
            "status_distribution": self.df['status'].value_counts().to_dict(),
            "avg_response_time_ms": round(self.df['time'].mean(), 2),
            "max_response_time_ms": self.df['time'].max(),
            "total_bytes_transferred": self.df['size'].sum()
        }
