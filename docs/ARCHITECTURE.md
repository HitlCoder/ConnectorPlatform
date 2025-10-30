# Connector Platform Architecture

## Overview

The Connector Platform is a modular, configuration-driven system for building and managing API connectors with OAuth 2.0 support. The platform enables rapid connector development through YAML configuration files that automatically generate working code.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        API Layer                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI REST API (connector_platform/api/main.py)   │  │
│  │  - Connector endpoints                                │  │
│  │  - Connection management                              │  │
│  │  - OAuth flow handlers                                │  │
│  │  - API proxy                                          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      Core Modules                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ OAuth        │  │ Connection   │  │ API Proxy    │      │
│  │ Manager      │  │ Manager      │  │              │      │
│  │              │  │              │  │              │      │
│  │ - Auth URL   │  │ - Create     │  │ - Execute    │      │
│  │ - Token      │  │ - Get        │  │ - Refresh    │      │
│  │   exchange   │  │ - Update     │  │ - Transform  │      │
│  │ - Refresh    │  │ - Delete     │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Connector    │  │ Config       │  │ Code         │      │
│  │ Registry     │  │ Validator    │  │ Generator    │      │
│  │              │  │              │  │              │      │
│  │ - Load       │  │ - Schema     │  │ - Python     │      │
│  │   configs    │  │   validation │  │ - Go         │      │
│  │ - List       │  │ - Type check │  │ - Templates  │      │
│  │ - Get        │  │              │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  PostgreSQL Database                                  │  │
│  │  - connections (connector instances)                  │  │
│  │  - oauth_tokens (access/refresh tokens)              │  │
│  │  - connector_metadata (optional storage)             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    SDK Layer                                 │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │  Python SDK      │         │  Go SDK          │          │
│  │  - BaseConnector │         │  - BaseConnector │          │
│  │  - Client        │         │  - Client        │          │
│  └──────────────────┘         └──────────────────┘          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                Configuration System                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  YAML Connector Configs                               │  │
│  │  connector_platform/config/connectors/                │  │
│  │  - gmail.yaml                                         │  │
│  │  - onedrive.yaml                                      │  │
│  │  - dropbox.yaml                                       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. OAuth Manager (`oauth_manager.py`)

Handles OAuth 2.0 authentication flows:

- **Authorization URL Generation**: Creates OAuth authorization URLs with proper scopes
- **Token Exchange**: Exchanges authorization codes for access tokens
- **Token Refresh**: Automatically refreshes expired access tokens
- **Expiry Tracking**: Monitors token expiration times

**Key Methods:**
- `generate_authorization_url()`: Create OAuth authorization URL
- `exchange_code_for_token()`: Exchange auth code for access token
- `refresh_access_token()`: Refresh an expired token
- `is_token_expired()`: Check if token needs refresh

### 2. Connection Manager (`connection_manager.py`)

Manages connector instances and their lifecycle:

- **CRUD Operations**: Create, read, update, delete connections
- **Token Storage**: Store and retrieve OAuth tokens
- **User Isolation**: Connections are scoped to users
- **Status Tracking**: Monitor connection health

**Key Methods:**
- `create_connection()`: Create new connector instance
- `get_connection()`: Retrieve connection details
- `list_connections()`: List user's connections
- `update_connection()`: Update connection properties
- `delete_connection()`: Remove connection and tokens
- `store_oauth_token()`: Save OAuth tokens
- `get_oauth_token()`: Retrieve active token

### 3. API Proxy (`api_proxy.py`)

Proxies API requests with automatic authentication:

- **Request Execution**: Makes authenticated API calls
- **Token Refresh**: Auto-refreshes expired tokens
- **Response Handling**: Handles JSON, binary, and text responses
- **Error Handling**: Comprehensive error reporting

**Features:**
- Automatic token injection
- Response type detection
- Binary content encoding (base64)
- Path parameter substitution
- Custom header support

### 4. Connector Registry (`connector_registry.py`)

Manages available connectors:

- **Config Loading**: Loads YAML connector configurations
- **Connector Lookup**: Fast connector retrieval
- **Endpoint Discovery**: Lists available endpoints
- **Version Management**: Tracks connector versions

### 5. Config Validator (`config_validator.py`)

Validates connector configurations:

- **Schema Validation**: Ensures configs match expected structure
- **Type Checking**: Validates parameter types
- **Required Fields**: Checks for mandatory fields
- **Pydantic Models**: Uses Pydantic for robust validation

### 6. Code Generator (`code_generator.py`)

Generates connector code from configurations:

- **Template-Based**: Uses Jinja2 templates
- **Multi-Language**: Supports Python and Go
- **Type-Safe**: Generates typed code
- **Documentation**: Includes docstrings and comments

## Data Flow

### OAuth Flow

```
1. User initiates OAuth
   ↓
2. Platform generates authorization URL
   ↓
3. User authorizes with provider
   ↓
4. Provider redirects with code
   ↓
5. Platform exchanges code for tokens
   ↓
6. Tokens stored in database
   ↓
7. Connection marked as active
```

### API Request Flow

```
1. Client requests data via SDK/API
   ↓
2. Platform retrieves connection & token
   ↓
3. Check if token expired
   ├─ Yes → Refresh token
   └─ No  → Continue
   ↓
4. Build authenticated request
   ↓
5. Execute API call
   ↓
6. Handle response (JSON/binary/text)
   ↓
7. Return to client
```

### Connector Creation Flow

```
1. Write YAML configuration
   ↓
2. Run code generator
   ↓
3. Connector code created
   ↓
4. Set environment variables
   ↓
5. Connector ready to use
```

## Database Schema

### connections

```sql
CREATE TABLE connections (
    id VARCHAR PRIMARY KEY,
    connector_type VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL,
    status VARCHAR DEFAULT 'active',
    config JSON DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### oauth_tokens

```sql
CREATE TABLE oauth_tokens (
    id VARCHAR PRIMARY KEY,
    connection_id VARCHAR NOT NULL,
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    token_type VARCHAR DEFAULT 'Bearer',
    expires_at TIMESTAMP,
    scope VARCHAR,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### connector_metadata

```sql
CREATE TABLE connector_metadata (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    display_name VARCHAR NOT NULL,
    description TEXT,
    version VARCHAR DEFAULT '1.0.0',
    auth_type VARCHAR NOT NULL,
    config_schema JSON NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## Security Considerations

1. **OAuth Credentials**: Stored in environment variables, never in code
2. **Token Storage**: Encrypted in database (implement encryption)
3. **Token Refresh**: Automatic refresh prevents exposure of long-lived tokens
4. **API Keys**: Never logged or exposed in responses
5. **HTTPS**: All external API calls use HTTPS
6. **Input Validation**: All inputs validated with Pydantic

## Scalability

- **Stateless API**: Scales horizontally
- **Connection Pooling**: Database connection pooling
- **Async Support**: Can be upgraded to async/await
- **Caching**: Can add Redis for token caching
- **Rate Limiting**: Can add per-connector rate limits

## Extension Points

1. **New Authentication Types**: Add to `AuthType` enum
2. **Custom Validators**: Extend `ConfigValidator`
3. **Response Transformers**: Add to `APIProxy`
4. **Webhook Support**: Add webhook handlers
5. **Event System**: Add event emitters for monitoring
