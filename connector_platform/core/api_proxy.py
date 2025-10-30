from typing import Dict, Optional, Any
import requests
from datetime import datetime


class APIProxy:
    def __init__(self, db_session, oauth_manager, connection_manager):
        self.db = db_session
        self.oauth_manager = oauth_manager
        self.connection_manager = connection_manager
    
    def execute_request(
        self,
        connection_id: str,
        connector_config: Dict,
        endpoint_config: Dict,
        params: Optional[Dict] = None,
        body: Optional[Dict] = None,
        path_params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        token = self.connection_manager.get_oauth_token(connection_id)
        
        if not token:
            return {
                "success": False,
                "error": "No authentication token found for this connection"
            }
        
        if self.oauth_manager.is_token_expired(token.expires_at):
            if token.refresh_token:
                try:
                    new_token = self.oauth_manager.refresh_access_token(
                        connector_config,
                        token.refresh_token
                    )
                    self.connection_manager.store_oauth_token(
                        connection_id,
                        new_token
                    )
                    token = self.connection_manager.get_oauth_token(connection_id)
                except Exception as e:
                    return {
                        "success": False,
                        "error": f"Failed to refresh token: {str(e)}"
                    }
            else:
                return {
                    "success": False,
                    "error": "Token expired and no refresh token available"
                }
        
        url = self._build_url(connector_config, endpoint_config, path_params)
        headers = self._build_headers(token, endpoint_config)
        method = endpoint_config.get("method", "GET").upper()
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=body if method in ["POST", "PUT", "PATCH"] else None,
                timeout=30
            )
            
            response_type = endpoint_config.get("response_type", "json")
            data = None
            
            if response.content:
                if response_type == "json":
                    try:
                        data = response.json()
                    except ValueError:
                        data = response.text
                elif response_type == "binary":
                    import base64
                    data = {
                        "content": base64.b64encode(response.content).decode('utf-8'),
                        "content_type": response.headers.get("Content-Type", "application/octet-stream")
                    }
                else:
                    data = response.text
            
            return {
                "success": response.status_code < 400,
                "status_code": response.status_code,
                "data": data,
                "headers": dict(response.headers)
            }
        
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _build_url(
        self,
        connector_config: Dict,
        endpoint_config: Dict,
        path_params: Optional[Dict] = None
    ) -> str:
        base_url = connector_config.get("base_url")
        path = endpoint_config.get("path")
        
        if path_params:
            for key, value in path_params.items():
                path = path.replace(f"{{{key}}}", str(value))
        
        return f"{base_url}{path}"
    
    def _build_headers(
        self,
        token,
        endpoint_config: Dict
    ) -> Dict[str, str]:
        headers = {
            "Authorization": f"{token.token_type} {token.access_token}",
            "Content-Type": "application/json"
        }
        
        custom_headers = endpoint_config.get("headers", {})
        headers.update(custom_headers)
        
        return headers
