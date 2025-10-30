"""
Base Connector Class for Connector Platform SDK
"""
from typing import Dict, Optional, Any
import requests


class BaseConnector:
    """
    Base class for all connectors in the platform.
    Provides common functionality for API calls and authentication.
    """
    
    def __init__(self, connection_id: str, config: Dict):
        self.connection_id = connection_id
        self.config = config
        self.connector_name = None
        self.base_url = None
        self.platform_url = config.get("platform_url", "http://localhost:5000")
    
    def execute_request(
        self,
        endpoint_config: Dict,
        params: Optional[Dict] = None,
        body: Optional[Dict] = None,
        path_params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Execute an API request through the platform proxy.
        
        Args:
            endpoint_config: Configuration for the endpoint (method, path, headers)
            params: Query parameters
            body: Request body for POST/PUT/PATCH requests
            path_params: Parameters to substitute in the path
        
        Returns:
            Dict containing the API response
        """
        proxy_url = f"{self.platform_url}/api/v1/proxy/execute"
        
        payload = {
            "connection_id": self.connection_id,
            "endpoint_config": endpoint_config,
            "params": params,
            "body": body,
            "path_params": path_params
        }
        
        try:
            response = requests.post(proxy_url, json=payload, timeout=30)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_connection_info(self) -> Dict[str, Any]:
        """Get information about the current connection."""
        url = f"{self.platform_url}/api/v1/connections/{self.connection_id}"
        
        try:
            response = requests.get(url, timeout=10)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }
