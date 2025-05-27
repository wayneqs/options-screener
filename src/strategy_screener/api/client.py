"""API client for external services."""
import requests
from urllib.parse import urlencode
from typing import Dict, Any, Optional
from ..config import config

class APIClient:
    """HTTP client for API calls."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
        })
        self.base_url = config.api_base_url
        self.timeout = config.api_timeout
        self.api_key = config.api_key


    def _build_url(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Build URL with API key parameter."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        # Start with API key parameter
        url_params = {'apikey': self.api_key}
        
        # Add any additional parameters
        if params:
            url_params.update(params)
        
        # Build the final URL with parameters
        return f"{url}?{urlencode(url_params)}"
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request."""
        url = self._build_url(endpoint, params)
        
        if config.debug:
            # Don't log the full URL with API key in production
            safe_url = url.replace(self.api_key, '*' * 8)
            print(f"GET {safe_url}")

        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise APIError(f"API request failed: {e}")
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make POST request."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"API request failed: {e}")

class APIError(Exception):
    """Custom exception for API errors."""
    pass

# Global client instance
api_client = APIClient()
