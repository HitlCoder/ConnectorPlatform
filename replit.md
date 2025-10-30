# Connector Platform - Project Information

## Overview

A comprehensive, modular connector platform with OAuth management, config-driven architecture, and multi-language SDK support. The platform enables rapid development of API connectors through configuration files that auto-generate connector code.

## Current State

The platform is fully implemented with:
- Core platform modules (OAuth manager, connection manager, API proxy, connector registry)
- Configuration-driven connector framework with YAML schemas
- Code generator for automatic connector creation
- Three pre-built connectors: Gmail, OneDrive, Dropbox
- Python SDK with base classes and client
- Go SDK with interfaces and client
- RESTful API with FastAPI
- PostgreSQL database for connections and tokens

## Recent Changes

- 2025-10-30: Initial platform implementation
  - Set up project structure and dependencies
  - Created database schema (connections, OAuth tokens, connector metadata)
  - Implemented core modules: OAuth manager, connection manager, API proxy, connector registry
  - Built configuration validator and code generator
  - Created connector configs for Gmail, OneDrive, Dropbox
  - Generated connector code from configurations
  - Built Python SDK (base_connector.py, client.py)
  - Built Go SDK (base_connector.go, client.go)
  - Implemented REST API endpoints
  - Added comprehensive documentation

## Architecture

### Platform Components

1. **Core Modules** (`platform/core/`)
   - `oauth_manager.py`: Handles OAuth 2.0 flows, token exchange, and refresh
   - `connection_manager.py`: Manages connection lifecycle and token storage
   - `api_proxy.py`: Proxies API requests with automatic authentication
   - `connector_registry.py`: Loads and manages connector configurations
   - `config_validator.py`: Validates connector configuration schemas
   - `code_generator.py`: Generates Python and Go connector code from configs

2. **Database** (`platform/database.py`)
   - Connection model: Stores connector instances per user
   - OAuthToken model: Stores access/refresh tokens with expiry
   - ConnectorMetadata model: Stores connector definitions

3. **API Layer** (`platform/api/main.py`)
   - FastAPI application with CORS support
   - Endpoints for connectors, connections, OAuth, and proxy
   - Automatic token refresh on requests

4. **SDKs**
   - Python SDK: BaseConnector class and ConnectorPlatformClient
   - Go SDK: BaseConnector struct and client package

5. **Configuration System**
   - YAML-based connector definitions in `platform/config/connectors/`
   - Supports OAuth 2.0, API endpoints with parameters
   - Parameter locations: query, body, path, header

### Key Features

- **Config-Driven**: New connectors require only a YAML file
- **Auto-Generation**: Code generator creates connector implementations
- **OAuth Management**: Complete OAuth 2.0 flow with token refresh
- **Multi-Language**: Python and Go SDKs
- **Modular**: Separated concerns for easy extension

## Project Structure

```
├── platform/
│   ├── core/              # Core platform modules
│   ├── api/               # REST API
│   ├── config/connectors/ # Connector YAML configs
│   ├── connectors/        # Generated connector code
│   └── database.py        # Database models
├── sdk/
│   ├── python/            # Python SDK
│   └── go/                # Go SDK
├── docs/                  # Documentation
├── main.py               # Application entry point
├── generate_connectors.py # Code generation script
└── README.md             # Main documentation
```

## Environment Variables Required

- `DATABASE_URL`: PostgreSQL connection string
- `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`: Gmail OAuth credentials
- `ONEDRIVE_CLIENT_ID`, `ONEDRIVE_CLIENT_SECRET`: OneDrive OAuth credentials
- `DROPBOX_CLIENT_ID`, `DROPBOX_CLIENT_SECRET`: Dropbox OAuth credentials

## How to Add a New Connector

1. Create YAML config in `platform/config/connectors/`
2. Run `python generate_connectors.py`
3. Set environment variables for OAuth credentials
4. Connector is ready to use via API and SDK

## Next Steps / Future Enhancements

- Add webhook support for real-time events
- Implement rate limiting per connector
- Create admin dashboard for monitoring
- Add connector versioning
- Build comprehensive testing framework
- Support additional auth methods (API keys, JWT, Basic)
- Create CLI tools for connector management
- Add logging and observability
