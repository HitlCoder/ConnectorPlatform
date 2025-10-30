"""
Connector Platform Client SDK
"""
from typing import Dict, List, Optional, Any
import requests


class ConnectorPlatformClient:
    """
    Client for interacting with the Connector Platform API.
    Manages connections, OAuth flows, and connector operations.
    """
    
    def __init__(self, platform_url: str = "http://localhost:5000"):
        self.platform_url = platform_url
        self.base_url = f"{platform_url}/api/v1"
    
    def list_connectors(self) -> List[Dict]:
        """List all available connectors."""
        url = f"{self.base_url}/connectors"
        response = requests.get(url)
        return response.json()
    
    def create_connection(
        self,
        connector_type: str,
        name: str,
        user_id: str,
        config: Optional[Dict] = None
    ) -> Dict:
        """Create a new connection for a connector."""
        url = f"{self.base_url}/connections"
        payload = {
            "connector_type": connector_type,
            "name": name,
            "user_id": user_id,
            "config": config or {}
        }
        response = requests.post(url, json=payload)
        return response.json()
    
    def get_connection(self, connection_id: str) -> Dict:
        """Get details of a specific connection."""
        url = f"{self.base_url}/connections/{connection_id}"
        response = requests.get(url)
        return response.json()
    
    def list_connections(
        self,
        user_id: str,
        connector_type: Optional[str] = None
    ) -> List[Dict]:
        """List connections for a user."""
        url = f"{self.base_url}/connections"
        params = {"user_id": user_id}
        if connector_type:
            params["connector_type"] = connector_type
        response = requests.get(url, params=params)
        return response.json()
    
    def delete_connection(self, connection_id: str) -> Dict:
        """Delete a connection."""
        url = f"{self.base_url}/connections/{connection_id}"
        response = requests.delete(url)
        return response.json()
    
    def initiate_oauth(
        self,
        connector_type: str,
        redirect_uri: str
    ) -> Dict:
        """Initiate OAuth flow for a connector."""
        url = f"{self.base_url}/oauth/authorize"
        payload = {
            "connector_type": connector_type,
            "redirect_uri": redirect_uri
        }
        response = requests.post(url, json=payload)
        return response.json()
    
    def complete_oauth(
        self,
        connection_id: str,
        code: str,
        redirect_uri: str
    ) -> Dict:
        """Complete OAuth flow with authorization code."""
        url = f"{self.base_url}/oauth/callback"
        payload = {
            "connection_id": connection_id,
            "code": code,
            "redirect_uri": redirect_uri
        }
        response = requests.post(url, json=payload)
        return response.json()
    
    def execute_connector_action(
        self,
        connection_id: str,
        endpoint_name: str,
        parameters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Execute a connector endpoint action."""
        url = f"{self.base_url}/connectors/execute"
        payload = {
            "connection_id": connection_id,
            "endpoint_name": endpoint_name,
            "parameters": parameters or {}
        }
        response = requests.post(url, json=payload)
        return response.json()
