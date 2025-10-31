# Connector Platform

A modular, configuration-driven platform for building and managing API connectors with OAuth support, SDK libraries in Python and Go, and auto-generated connector code.

## Features

- **Config-Driven Architecture**: Define connectors using simple YAML configuration files
- **Automatic Code Generation**: Generate connector code from configurations for Python and Go
- **OAuth 2.0 Management**: Built-in OAuth flow handling with token storage and automatic refresh
- **Connection Management**: Create, manage, and monitor multiple connector instances
- **API Proxy Layer**: Transparent request/response handling with authentication
- **Data Transformation**: Automatic transformation of API responses to common data models
- **Kafka Integration**: Publish transformed data to Kafka topics organized by connector type
- **Multi-Language SDKs**: Python and Go SDKs for building custom connectors
- **RESTful API**: Complete REST API for all platform operations
- **Developer Dashboard**: Modern web UI for managing connectors, connections, and testing APIs
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
├── frontend/              # Developer Dashboard UI
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── api/           # API client
│   │   ├── App.tsx        # Main application
│   │   └── main.tsx       # Entry point
│   ├── vite.config.ts     # Vite configuration
│   └── package.json       # Frontend dependencies
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
│   ├── DASHBOARD_GUIDE.md # Dashboard user guide
│   └── ...
├── main.py               # Application entry point
└── generate_connectors.py # Code generation script
```

## Quick Start

### Prerequisites

**Option 1: Docker (Recommended for local development) 🐳**
- Docker Desktop installed
- No other dependencies needed!

**Option 2: Manual Setup**
- Python 3.11+
- PostgreSQL database
- Node.js 18+ (for dashboard)

### Installation

#### Option 1: Docker Setup (Easiest)

**One command to run everything:**

```bash
docker-compose up -d
```

This starts:
- PostgreSQL database
- Backend API (port 8000)
- Frontend dashboard (port 5000)

**Access the application:**
- Dashboard: http://localhost:5000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**For complete Docker documentation, see [docker-setup.md](docker-setup.md)**

#### Option 2: Manual Backend Setup

1. Install Python dependencies:
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

3. Start the backend API:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

#### Frontend Dashboard Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

The dashboard will be available at `http://localhost:5000`

#### Production Build

For production deployment:

```bash
# Build frontend
cd frontend
npm run build

# The built files will be in frontend/dist/
# Serve them using your preferred static file server
```

### Using the Developer Dashboard

The platform includes a comprehensive web-based dashboard for managing connectors and connections:

1. **Browse Connectors** - View all available integrations (Gmail, OneDrive, Dropbox)
2. **Manage Connections** - Create, authorize, and manage connector instances
3. **Test APIs** - Interactive endpoint testing with parameter input and formatted responses
4. **OAuth Flow** - Automated OAuth authorization with secure token management

**Access the dashboard at:** `http://localhost:5000`

See the complete [Dashboard Guide](docs/DASHBOARD_GUIDE.md) for detailed usage instructions.

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
client = ConnectorPlatformClient("http://localhost:8000")

# List connectors
connectors = client.list_connectors()

# Create connection
connection = client.create_connection("gmail", "My Gmail", "user123")

# Custom connector
from platform.connectors.gmail_connector import GmailConnector

gmail = GmailConnector(
    connection_id="conn-123",
    config={"platform_url": "http://localhost:8000"}
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
c := client.NewClient("http://localhost:8000")

// List connectors
connectors, _ := c.ListConnectors()

// Create connection
conn, _ := c.CreateConnection("gmail", "My Gmail", "user123", nil)

// Use connector
// Custom implementation based on generated code
```

## Developer Dashboard

The platform includes a modern web-based dashboard built with React, TypeScript, and Vite.

### Dashboard Features

- **Connectors View**: Browse all available connectors with details
- **Connections Management**: Create, view, and delete connections
- **OAuth Integration**: Seamless OAuth 2.0 authorization flow
- **API Tester**: Interactive endpoint testing with parameter inputs and JSON response viewing
- **Responsive Design**: Clean, professional UI that works on all devices

### Dashboard Technology Stack

- React 19 + TypeScript
- Vite 7 (build tool)
- React Router DOM 7 (routing)
- Axios (HTTP client)
- Custom CSS styling

### Running the Dashboard

```bash
cd frontend
npm install
npm run dev
```

Dashboard available at: `http://localhost:5000`

For complete dashboard documentation, see [DASHBOARD_GUIDE.md](docs/DASHBOARD_GUIDE.md)

## Data Transformation and Kafka Publishing

The platform automatically transforms API responses from different connectors into common data models and publishes them to Kafka topics.

### Connector Types

Connectors are classified by type:
- **`cloud_storage`**: OneDrive, Dropbox, Google Drive
- **`email`**: Gmail, Outlook
- **`marketing`**: Marketo, Klaviyo, Mailchimp

### Common Data Models

Each type has standardized models:

**Cloud Storage**:
```json
{
  "files": [
    {
      "id": "file-id",
      "name": "document.pdf",
      "path": "/folder/document.pdf",
      "size": 1024000,
      "modified_at": "2025-01-15T14:30:00Z",
      "is_folder": false
    }
  ],
  "total_count": 42
}
```

**Email**:
```json
{
  "messages": [
    {
      "id": "msg-id",
      "subject": "Meeting Tomorrow",
      "from_address": "sender@example.com",
      "received_at": "2025-01-15T10:00:00Z",
      "is_read": false
    }
  ]
}
```

### Kafka Topics

Transformed data is published to topics by type:
- `connector-platform.cloud_storage`
- `connector-platform.email`
- `connector-platform.marketing`

### Configuration

```bash
# Enable Kafka (default: false, uses mock publisher)
export KAFKA_ENABLED=true
export KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

### Example Response

```json
{
  "success": true,
  "data": { /* Raw API response */ },
  "transformed_data": { /* Common format */ },
  "connector_type": "cloud_storage",
  "published_to_kafka": true
}
```

For detailed documentation, see [TRANSFORMATION_AND_KAFKA.md](docs/TRANSFORMATION_AND_KAFKA.md)

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
