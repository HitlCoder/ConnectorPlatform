# Connector Platform

A modular, configuration-driven platform for building and managing API connectors with OAuth support, SDK libraries in Python and Go, and auto-generated connector code.

## Features

- **Config-Driven Architecture**: Define connectors using simple YAML configuration files
- **Automatic Code Generation**: Generate connector code from configurations for Python and Go
- **OAuth 2.0 Management**: Built-in OAuth flow handling with token storage and automatic refresh
- **Connection Management**: Create, manage, and monitor multiple connector instances
- **API Proxy Layer**: Transparent request/response handling with authentication
- **Multi-Language SDKs**: Python and Go SDKs for building custom connectors
- **RESTful API**: Complete REST API for all platform operations
- **Pre-built Connectors**: Gmail, OneDrive, and Dropbox connectors included

## Project Structure

```
├── platform/
│   ├── core/              # Core platform modules
│   │   ├── oauth_manager.py
│   │   ├── connection_manager.py
│   │   ├── api_proxy.py
│   │   ├── connector_registry.py
│   │   ├── config_validator.py
│   │   └── code_generator.py
│   ├── api/               # REST API endpoints
│   │   └── main.py
│   ├── config/            # Connector configurations
│   │   └── connectors/
│   │       ├── gmail.yaml
│   │       ├── onedrive.yaml
│   │       └── dropbox.yaml
│   ├── connectors/        # Generated connector code
│   │   ├── gmail_connector.py
│   │   ├── onedrive_connector.py
│   │   └── dropbox_connector.py
│   └── database.py        # Database models
├── sdk/
│   ├── python/            # Python SDK
│   │   ├── base_connector.py
│   │   └── client.py
│   └── go/                # Go SDK
│       ├── connector/
│       │   └── base_connector.go
│       └── client/
│           └── client.go
├── docs/                  # Documentation
├── main.py               # Application entry point
└── generate_connectors.py # Code generation script
```

## Quick Start

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export DATABASE_URL="postgresql://..."
export GMAIL_CLIENT_ID="your-gmail-client-id"
export GMAIL_CLIENT_SECRET="your-gmail-client-secret"
export ONEDRIVE_CLIENT_ID="your-onedrive-client-id"
export ONEDRIVE_CLIENT_SECRET="your-onedrive-client-secret"
export DROPBOX_CLIENT_ID="your-dropbox-client-id"
export DROPBOX_CLIENT_SECRET="your-dropbox-client-secret"
```

3. Start the platform:
```bash
python main.py
```

The API will be available at `http://localhost:5000`

### Creating a New Connector

1. **Create a configuration file** in `platform/config/connectors/`:

```yaml
# myservice.yaml
name: myservice
display_name: My Service
description: Connect to My Service API
version: 1.0.0
base_url: https://api.myservice.com/v1

auth:
  type: oauth2
  auth_url: https://myservice.com/oauth/authorize
  token_url: https://myservice.com/oauth/token
  scope:
    - read
    - write
  client_id_env: MYSERVICE_CLIENT_ID
  client_secret_env: MYSERVICE_CLIENT_SECRET

endpoints:
  - name: list_items
    display_name: List Items
    description: Get a list of items
    method: GET
    path: /items
    parameters:
      - name: limit
        type: int
        required: false
        description: Maximum number of items
        location: query
        default: 10
    response_type: json

  - name: create_item
    display_name: Create Item
    description: Create a new item
    method: POST
    path: /items
    parameters:
      - name: name
        type: str
        required: true
        description: Item name
        location: body
      - name: description
        type: str
        required: false
        description: Item description
        location: body
    response_type: json
```

2. **Generate connector code**:

```bash
python generate_connectors.py
```

This automatically creates:
- `platform/connectors/myservice_connector.py`
- Python and Go connector implementations

3. **Use the connector** via the API or SDK:

```python
from sdk.python import ConnectorPlatformClient

client = ConnectorPlatformClient()

# Create connection
connection = client.create_connection(
    connector_type="myservice",
    name="My Service Connection",
    user_id="user123"
)

# Complete OAuth flow
oauth_info = client.initiate_oauth("myservice", "http://localhost:3000/callback")
# ... redirect user to oauth_info['authorization_url']
# ... on callback, complete OAuth:
client.complete_oauth(connection["id"], code, "http://localhost:3000/callback")

# Execute connector actions
result = client.execute_connector_action(
    connection_id=connection["id"],
    endpoint_name="list_items",
    parameters={"limit": 20}
)
```

## API Endpoints

### Connectors

- `GET /api/v1/connectors` - List all available connectors
- `GET /api/v1/connectors/{name}` - Get connector details
- `GET /api/v1/connectors/{name}/endpoints` - List connector endpoints

### Connections

- `POST /api/v1/connections` - Create a new connection
- `GET /api/v1/connections/{id}` - Get connection details
- `GET /api/v1/connections?user_id={id}` - List user connections
- `DELETE /api/v1/connections/{id}` - Delete a connection

### OAuth

- `POST /api/v1/oauth/authorize` - Initiate OAuth flow
- `POST /api/v1/oauth/callback` - Complete OAuth flow

### Proxy

- `POST /api/v1/proxy/execute` - Execute API request through proxy

## SDK Usage

### Python SDK

```python
from sdk.python import ConnectorPlatformClient, BaseConnector

# Platform client
client = ConnectorPlatformClient("http://localhost:5000")

# List connectors
connectors = client.list_connectors()

# Create connection
connection = client.create_connection("gmail", "My Gmail", "user123")

# Custom connector
from platform.connectors.gmail_connector import GmailConnector

gmail = GmailConnector(
    connection_id="conn-123",
    config={"platform_url": "http://localhost:5000"}
)

messages = gmail.list_messages(maxResults=10)
```

### Go SDK

```go
import (
    "github.com/connector-platform/sdk/go/client"
    "github.com/connector-platform/sdk/go/connector"
)

// Create client
c := client.NewClient("http://localhost:5000")

// List connectors
connectors, _ := c.ListConnectors()

// Create connection
conn, _ := c.CreateConnection("gmail", "My Gmail", "user123", nil)

// Use connector
// Custom implementation based on generated code
```

## Configuration Schema

Each connector configuration must include:

- `name`: Unique connector identifier
- `display_name`: Human-readable name
- `base_url`: API base URL
- `auth`: Authentication configuration
  - `type`: Authentication type (oauth2, api_key, basic)
  - `auth_url`: OAuth authorization URL
  - `token_url`: OAuth token URL
  - `scope`: OAuth scopes
  - `client_id_env`: Environment variable for client ID
  - `client_secret_env`: Environment variable for client secret
- `endpoints`: List of API endpoints
  - `name`: Endpoint identifier
  - `method`: HTTP method (GET, POST, PUT, DELETE, PATCH)
  - `path`: API path (supports {param} placeholders)
  - `parameters`: List of parameters with location (query, body, path, header)

## Database Schema

The platform uses PostgreSQL with the following tables:

- **connections**: Stores connection instances
- **oauth_tokens**: Stores OAuth access and refresh tokens
- **connector_metadata**: Stores connector configurations

## Development

### Adding New Features

1. Extend core modules in `platform/core/`
2. Update API endpoints in `platform/api/main.py`
3. Regenerate connector code with `python generate_connectors.py`
4. Update SDK libraries if needed

### Testing

The platform includes configuration validation and error handling. Test your connectors:

1. Create a connection via API
2. Complete OAuth flow
3. Execute connector actions
4. Verify responses

## License

MIT License
