from typing import Dict, List, Optional
import yaml
import os
from pathlib import Path


class ConnectorRegistry:
    def __init__(self):
        self.connectors: Dict[str, Dict] = {}
        self.config_dir = Path("platform/config/connectors")
    
    def load_connector_configs(self):
        if not self.config_dir.exists():
            return
        
        for config_file in self.config_dir.glob("*.yaml"):
            try:
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)
                    connector_name = config.get("name")
                    if connector_name:
                        self.connectors[connector_name] = config
            except Exception as e:
                print(f"Error loading connector config {config_file}: {e}")
    
    def register_connector(self, name: str, config: Dict):
        self.connectors[name] = config
    
    def get_connector(self, name: str) -> Optional[Dict]:
        return self.connectors.get(name)
    
    def list_connectors(self) -> List[Dict]:
        return [
            {
                "name": name,
                "display_name": config.get("display_name", name),
                "description": config.get("description", ""),
                "auth_type": config.get("auth", {}).get("type"),
                "version": config.get("version", "1.0.0")
            }
            for name, config in self.connectors.items()
        ]
    
    def get_connector_endpoints(self, name: str) -> List[Dict]:
        connector = self.get_connector(name)
        if not connector:
            return []
        
        return connector.get("endpoints", [])
    
    def get_endpoint(self, connector_name: str, endpoint_name: str) -> Optional[Dict]:
        endpoints = self.get_connector_endpoints(connector_name)
        
        for endpoint in endpoints:
            if endpoint.get("name") == endpoint_name:
                return endpoint
        
        return None
