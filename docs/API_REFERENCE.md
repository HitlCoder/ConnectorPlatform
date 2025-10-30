# API Reference

Complete API documentation for the Connector Platform.

## Base URL

```
http://localhost:5000/api/v1
```

## Authentication

Currently, all endpoints are public. Authentication/authorization will be added in future versions.

## Endpoints

### Connectors

#### List All Connectors

```
GET /api/v1/connectors
```

Returns a list of all available connectors.

**Response:**
```json
[
  {
    "name": "gmail",
    "display_name": "Gmail",
    "description": "Connect to Gmail to send, read, and manage emails",
    "auth_type": "oauth2",
    "version": "1.0.0"
  }
]
```

#### Get Connector Details

```
GET /api/v1/connectors/{connector_name}
```

**Parameters:**
- `connector_name` (path): Connector identifier

**Response:**
```json
{
  "name": "gmail",
  "display_name": "Gmail",
  "description": "Connect to Gmail",
  "version": "1.0.0",
  "base_url": "https://gmail.googleapis.com",
  "auth": { ... },
  "endpoints": [ ... ]
}
```

#### List Connector Endpoints

```
GET /api/v1/connectors/{connector_name}/endpoints
```

**Parameters:**
- `connector_name` (path): Connector identifier

**Response:**
```json
[
  {
    "name": "list_messages",
    "display_name": "List Messages",
    "description": "List messages in mailbox",
    "method": "GET",
    "path": "/gmail/v1/users/me/messages",
    "parameters": [ ... ]
  }
]
```

### Connections

#### Create Connection

```
POST /api/v1/connections
```

**Request Body:**
```json
{
  "connector_type": "gmail",
  "name": "My Gmail Connection",
  "user_id": "user123",
  "config": {}
}
```

**Response:**
```json
{
  "id": "conn-uuid",
  "connector_type": "gmail",
  "name": "My Gmail Connection",
  "user_id": "user123",
  "status": "pending",
  "config": {},
  "created_at": "2025-10-30T12:00:00"
}
```

#### Get Connection

```
GET /api/v1/connections/{connection_id}
```

**Parameters:**
- `connection_id` (path): Connection UUID

**Response:**
```json
{
  "id": "conn-uuid",
  "connector_type": "gmail",
  "name": "My Gmail Connection",
  "user_id": "user123",
  "status": "active",
  "config": {},
  "created_at": "2025-10-30T12:00:00",
  "updated_at": "2025-10-30T12:05:00"
}
```

#### List Connections

```
GET /api/v1/connections?user_id={user_id}&connector_type={connector_type}
```

**Parameters:**
- `user_id` (query, required): User identifier
- `connector_type` (query, optional): Filter by connector type

**Response:**
```json
[
  {
    "id": "conn-uuid",
    "connector_type": "gmail",
    "name": "My Gmail Connection",
    "status": "active",
    "created_at": "2025-10-30T12:00:00"
  }
]
```

#### Delete Connection

```
DELETE /api/v1/connections/{connection_id}
```

**Parameters:**
- `connection_id` (path): Connection UUID

**Response:**
```json
{
  "message": "Connection deleted successfully"
}
```

### OAuth

#### Initiate OAuth Flow

```
POST /api/v1/oauth/authorize
```

**Request Body:**
```json
{
  "connector_type": "gmail",
  "redirect_uri": "http://localhost:3000/callback",
  "connection_id": "conn-uuid"
}
```

**Response:**
```json
{
  "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?...",
  "state": "random-state-string",
  "connection_id": "conn-uuid"
}
```

**Usage:**
1. Redirect user to `authorization_url`
2. User authorizes the application
3. Service redirects back to `redirect_uri` with `code` parameter
4. Use code in callback endpoint

#### Complete OAuth Flow

```
POST /api/v1/oauth/callback
```

**Request Body:**
```json
{
  "connection_id": "conn-uuid",
  "code": "authorization-code",
  "redirect_uri": "http://localhost:3000/callback"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OAuth flow completed successfully",
  "connection_id": "conn-uuid"
}
```

### Proxy

#### Execute API Request

```
POST /api/v1/proxy/execute
```

Execute an API request through the platform proxy with automatic authentication.

**Request Body:**
```json
{
  "connection_id": "conn-uuid",
  "endpoint_config": {
    "method": "GET",
    "path": "/gmail/v1/users/me/messages",
    "headers": {}
  },
  "params": {
    "maxResults": 10
  },
  "body": null,
  "path_params": null
}
```

**Response:**
```json
{
  "success": true,
  "status_code": 200,
  "data": {
    "messages": [ ... ],
    "nextPageToken": "..."
  },
  "headers": { ... }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message"
}
```

## Health Check

```
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

## Error Codes

- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error

## Rate Limiting

Currently not implemented. Future versions will include rate limiting per connection.

## Webhooks

Not yet implemented. Future versions will support webhook subscriptions for real-time events.
