# Connector Platform Go SDK

A Go SDK for building and interacting with connectors on the Connector Platform.

## Installation

```bash
go get github.com/connector-platform/sdk/go
```

## Quick Start

### Using the Platform Client

```go
package main

import (
    "fmt"
    "github.com/connector-platform/sdk/go/client"
)

func main() {
    // Create client
    c := client.NewClient("http://localhost:5000")
    
    // List available connectors
    connectors, err := c.ListConnectors()
    if err != nil {
        panic(err)
    }
    fmt.Printf("Available connectors: %+v\n", connectors)
    
    // Create a connection
    connection, err := c.CreateConnection(
        "gmail",
        "My Gmail Connection",
        "user123",
        make(map[string]interface{}),
    )
    if err != nil {
        panic(err)
    }
    
    // Initiate OAuth flow
    oauthResp, err := c.InitiateOAuth("gmail", "http://localhost:3000/callback")
    if err != nil {
        panic(err)
    }
    fmt.Printf("Visit: %s\n", oauthResp.AuthorizationURL)
    
    // After user authorizes, complete OAuth
    result, err := c.CompleteOAuth(
        connection.ID,
        "authorization_code_from_callback",
        "http://localhost:3000/callback",
    )
    if err != nil {
        panic(err)
    }
    fmt.Printf("OAuth complete: %+v\n", result)
}
```

### Building a Custom Connector

```go
package connectors

import (
    "github.com/connector-platform/sdk/go/connector"
)

type MyCustomConnector struct {
    connector.BaseConnector
}

func NewMyCustomConnector(connectionID string, config map[string]interface{}) *MyCustomConnector {
    return &MyCustomConnector{
        BaseConnector: connector.BaseConnector{
            ConnectionID:  connectionID,
            Config:        config,
            ConnectorName: "my_custom_connector",
            BaseURL:       "https://api.example.com",
        },
    }
}

func (c *MyCustomConnector) ListItems(limit int) (map[string]interface{}, error) {
    endpointConfig := map[string]interface{}{
        "method": "GET",
        "path":   "/items",
    }
    
    params := map[string]interface{}{
        "limit": limit,
    }
    
    return c.ExecuteRequest(endpointConfig, params, nil, nil)
}

func (c *MyCustomConnector) CreateItem(name, description string) (map[string]interface{}, error) {
    endpointConfig := map[string]interface{}{
        "method": "POST",
        "path":   "/items",
    }
    
    body := map[string]interface{}{
        "name":        name,
        "description": description,
    }
    
    return c.ExecuteRequest(endpointConfig, nil, body, nil)
}
```

## Features

- **Connection Management**: Create, retrieve, and delete connections
- **OAuth 2.0 Support**: Built-in OAuth flow handling
- **Base Connector**: Embed to create custom connectors quickly
- **Type Safety**: Strongly typed client and responses
- **Error Handling**: Comprehensive error handling

## API Reference

### ConnectorPlatformClient

- `ListConnectors()`: Get all available connectors
- `CreateConnection(connectorType, name, userID, config)`: Create a new connection
- `GetConnection(connectionID)`: Get connection details
- `DeleteConnection(connectionID)`: Delete a connection
- `InitiateOAuth(connectorType, redirectURI)`: Start OAuth flow
- `CompleteOAuth(connectionID, code, redirectURI)`: Complete OAuth flow

### BaseConnector

- `ExecuteRequest(endpointConfig, params, body, pathParams)`: Execute API request
- `GetConnectionInfo()`: Get connection information
