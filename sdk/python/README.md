# Connector Platform Python SDK

A Python SDK for building and interacting with connectors on the Connector Platform.

## Installation

```bash
pip install connector-platform-sdk
```

## Quick Start

### Using the Platform Client

```python
from sdk.python import ConnectorPlatformClient

client = ConnectorPlatformClient(platform_url="http://localhost:5000")

# List available connectors
connectors = client.list_connectors()

# Create a connection
connection = client.create_connection(
    connector_type="gmail",
    name="My Gmail Connection",
    user_id="user123"
)

# Initiate OAuth flow
oauth_info = client.initiate_oauth(
    connector_type="gmail",
    redirect_uri="http://localhost:3000/callback"
)
print(f"Visit: {oauth_info['authorization_url']}")

# After user authorizes, complete OAuth
result = client.complete_oauth(
    connection_id=connection["id"],
    code="authorization_code_from_callback",
    redirect_uri="http://localhost:3000/callback"
)
```

### Building a Custom Connector

```python
from sdk.python import BaseConnector

class MyCustomConnector(BaseConnector):
    def __init__(self, connection_id: str, config: dict):
        super().__init__(connection_id, config)
        self.connector_name = "my_custom_connector"
        self.base_url = "https://api.example.com"
    
    def list_items(self, limit: int = 10):
        endpoint_config = {
            "method": "GET",
            "path": "/items"
        }
        params = {"limit": limit}
        return self.execute_request(endpoint_config, params=params)
    
    def create_item(self, name: str, description: str):
        endpoint_config = {
            "method": "POST",
            "path": "/items"
        }
        body = {"name": name, "description": description}
        return self.execute_request(endpoint_config, body=body)

# Use the connector
connector = MyCustomConnector(
    connection_id="conn-123",
    config={"platform_url": "http://localhost:5000"}
)
result = connector.list_items(limit=20)
```

## Features

- **Easy Connection Management**: Create, list, and delete connections
- **OAuth 2.0 Support**: Built-in OAuth flow handling
- **Base Connector Class**: Extend to create custom connectors quickly
- **Type Hints**: Full type annotation support
- **Error Handling**: Comprehensive error responses

## API Reference

### ConnectorPlatformClient

- `list_connectors()`: Get all available connectors
- `create_connection(connector_type, name, user_id, config)`: Create a new connection
- `get_connection(connection_id)`: Get connection details
- `list_connections(user_id, connector_type)`: List user connections
- `delete_connection(connection_id)`: Delete a connection
- `initiate_oauth(connector_type, redirect_uri)`: Start OAuth flow
- `complete_oauth(connection_id, code, redirect_uri)`: Complete OAuth flow

### BaseConnector

- `execute_request(endpoint_config, params, body, path_params)`: Execute API request
- `get_connection_info()`: Get connection information
