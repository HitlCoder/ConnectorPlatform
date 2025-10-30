"""
Utility functions for the connector platform
"""
import os
from typing import Dict


def build_connector_auth_config(connector: Dict) -> Dict:
    """
    Build a connector authentication configuration by loading credentials
    from environment variables specified in the connector config.
    
    Args:
        connector: Connector configuration dictionary
    
    Returns:
        Dictionary with OAuth configuration including client_id and client_secret
    """
    auth_config = connector.get("auth", {})
    
    client_id = os.getenv(auth_config.get("client_id_env", ""))
    client_secret = os.getenv(auth_config.get("client_secret_env", ""))
    
    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "auth_url": auth_config.get("auth_url"),
        "token_url": auth_config.get("token_url"),
        "scope": auth_config.get("scope", []),
        "base_url": connector.get("base_url")
    }


def validate_credentials(client_id: str, client_secret: str, client_id_env: str, client_secret_env: str) -> tuple[bool, str]:
    """
    Validate that OAuth credentials are configured.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not client_id or not client_secret:
        return False, f"OAuth credentials not configured. Set {client_id_env} and {client_secret_env}"
    return True, ""
