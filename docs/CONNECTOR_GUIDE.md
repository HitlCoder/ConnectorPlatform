# Connector Development Guide

This guide explains how to create new connectors for the Connector Platform.

## Overview

Creating a new connector involves three simple steps:
1. Write a YAML configuration file
2. Generate the connector code
3. Configure OAuth credentials

## Step 1: Create Configuration File

Create a YAML file in `connector_platform/config/connectors/` with the following structure:

```yaml
name: myconnector
display_name: My Connector
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
  client_id_env: MYCONNECTOR_CLIENT_ID
  client_secret_env: MYCONNECTOR_CLIENT_SECRET

endpoints:
  - name: list_items
    display_name: List Items
    description: Retrieve a list of items
    method: GET
    path: /items
    parameters:
      - name: limit
        type: int
        required: false
        description: Maximum number of items to return
        location: query
        default: 10
    response_type: json
```

## Configuration Schema

### Root Level Fields

- **name** (required): Unique identifier for the connector (alphanumeric with underscores/hyphens)
- **display_name** (required): Human-readable name shown in UI
- **description**: Brief description of what the connector does
- **version**: Semantic version (default: "1.0.0")
- **base_url** (required): Base URL for all API requests

### Auth Configuration

- **type**: Authentication type (`oauth2`, `api_key`, `basic`)
- **auth_url**: OAuth authorization endpoint
- **token_url**: OAuth token exchange endpoint
- **scope**: List of OAuth scopes to request
- **client_id_env**: Environment variable name for client ID
- **client_secret_env**: Environment variable name for client secret

### Endpoint Configuration

Each endpoint requires:

- **name** (required): Method name in generated code
- **display_name** (required): Human-readable endpoint name
- **description**: What this endpoint does
- **method** (required): HTTP method (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`)
- **path** (required): API path (can include `{parameter}` placeholders)
- **parameters**: List of parameters (see below)
- **response_type**: Response format (`json`, `binary`, `text`)
- **headers**: Custom headers as key-value pairs

### Parameter Configuration

- **name** (required): Parameter name
- **type** (required): Data type (`str`, `int`, `bool`, `list`, `dict`)
- **required**: Whether parameter is required (default: false)
- **description**: Parameter description
- **location** (required): Where to send parameter:
  - `query`: URL query parameter
  - `body`: Request body field
  - `path`: URL path parameter (must be in endpoint path)
  - `header`: HTTP header
- **default**: Default value if not provided

## Step 2: Generate Connector Code

Run the code generator:

```bash
python generate_connectors.py
```

This creates:
- `connector_platform/connectors/myconnector_connector.py` - Python implementation
- `connector_platform/connectors/go/myconnector_connector.go` - Go implementation

## Step 3: Configure OAuth Credentials

### Get OAuth Credentials

1. Register your application with the service provider
2. Get client ID and client secret
3. Set redirect URI to your callback URL

### Set Environment Variables

```bash
export MYCONNECTOR_CLIENT_ID="your-client-id"
export MYCONNECTOR_CLIENT_SECRET="your-client-secret"
```

## Using Your Connector

### Via Python SDK

```python
from sdk.python import ConnectorPlatformClient

client = ConnectorPlatformClient("http://localhost:5000")

# Create connection
connection = client.create_connection(
    connector_type="myconnector",
    name="My Connection",
    user_id="user123"
)

# Initiate OAuth
oauth = client.initiate_oauth(
    connector_type="myconnector",
    redirect_uri="http://localhost:3000/callback"
)

print(f"Visit: {oauth['authorization_url']}")

# After user authorizes, complete OAuth
result = client.complete_oauth(
    connection_id=connection["id"],
    code="auth_code_from_callback",
    redirect_uri="http://localhost:3000/callback"
)

# Use the connector
from connector_platform.connectors.myconnector_connector import MyconnectorConnector

connector = MyconnectorConnector(
    connection_id=connection["id"],
    config={"platform_url": "http://localhost:5000"}
)

items = connector.list_items(limit=20)
```

### Via REST API

```bash
# List available connectors
curl http://localhost:5000/api/v1/connectors

# Create connection
curl -X POST http://localhost:5000/api/v1/connections \
  -H "Content-Type: application/json" \
  -d '{
    "connector_type": "myconnector",
    "name": "My Connection",
    "user_id": "user123"
  }'

# Initiate OAuth
curl -X POST http://localhost:5000/api/v1/oauth/authorize \
  -H "Content-Type: application/json" \
  -d '{
    "connector_type": "myconnector",
    "redirect_uri": "http://localhost:3000/callback"
  }'

# Complete OAuth (after user authorizes)
curl -X POST http://localhost:5000/api/v1/oauth/callback \
  -H "Content-Type: application/json" \
  -d '{
    "connection_id": "conn-id",
    "code": "authorization-code",
    "redirect_uri": "http://localhost:3000/callback"
  }'

# Execute connector action
curl -X POST http://localhost:5000/api/v1/proxy/execute \
  -H "Content-Type: application/json" \
  -d '{
    "connection_id": "conn-id",
    "endpoint_config": {
      "method": "GET",
      "path": "/items"
    },
    "params": {"limit": 20}
  }'
```

## Advanced Topics

### Path Parameters

Use `{parameter}` syntax in the path:

```yaml
- name: get_item
  path: /items/{itemId}
  parameters:
    - name: itemId
      type: str
      required: true
      location: path
```

### Custom Headers

Add headers to specific endpoints:

```yaml
- name: upload_file
  method: POST
  path: /upload
  headers:
    Content-Type: application/octet-stream
    X-Custom-Header: value
```

### Complex Body Parameters

For nested JSON in request body:

```yaml
- name: create_item
  method: POST
  path: /items
  parameters:
    - name: name
      type: str
      location: body
    - name: metadata
      type: dict
      location: body
```

## Validation

The platform validates your configuration before generating code. Common errors:

- Invalid connector name (must be alphanumeric with underscores/hyphens)
- Missing required fields
- Invalid HTTP method
- Invalid parameter location
- Path parameters not in path string

## Examples

See the included connectors for reference:
- `connector_platform/config/connectors/gmail.yaml` - Gmail API
- `connector_platform/config/connectors/onedrive.yaml` - OneDrive API
- `connector_platform/config/connectors/dropbox.yaml` - Dropbox API
